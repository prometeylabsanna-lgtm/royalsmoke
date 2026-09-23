from decimal import Decimal

from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.api.serializers.auth_cart import (
    CartItemPatchSerializer,
    CartItemWriteSerializer,
    LoginSerializer,
    RegisterSerializer,
)
from apps.api.serializers.orders import CheckoutSerializer, OrderDetailSerializer
from apps.cart import db_services as db_cart
from apps.cart import services as session_cart
from apps.core.currency import convert_cart_totals
from apps.orders.models import Order, OrderItem
from apps.orders.services import notify_order_created
from apps.orders.services import payments as pay_svc

User = get_user_model()


class AnonCheckoutThrottle(AnonRateThrottle):
    scope = 'anon_checkout'


def _serialize_cart_payload(totals: dict) -> dict:
    priced = convert_cart_totals(totals)
    items = []
    for item in priced['items']:
        items.append({
            'id': item.get('id'),
            'key': item['key'],
            'product_id': item['product'].id,
            'product_name': str(item['product']),
            'quantity': item['quantity'],
            'unit_price': str(item['unit_price']),
            'line_total': str(item['line_total']),
        })
    return {
        'items': items,
        'subtotal': str(priced['subtotal']),
        'count': priced['count'],
        'total': str(priced['total']),
        'currency': priced['currency'],
    }


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        if User.objects.filter(email__iexact=data['email']).exists():
            return Response({'detail': 'Email already registered'}, status=400)
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name') or '',
            last_name=data.get('last_name') or '',
            phone=data.get('phone') or '',
        )
        token, _ = Token.objects.get_or_create(user=user)
        db_cart.merge_session_into_user(request.session, user)
        return Response({'token': token.key, 'email': user.email}, status=201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=ser.validated_data['email'],
            password=ser.validated_data['password'],
        )
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        db_cart.merge_session_into_user(request.session, user)
        return Response({'token': token.key, 'email': user.email})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'ok'})


class CartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            totals = db_cart.cart_totals(request.user)
        else:
            totals = session_cart.cart_totals(request.session)
        return Response(_serialize_cart_payload(totals))

    def post(self, request):
        ser = CartItemWriteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        if request.user.is_authenticated:
            db_cart.add_item(
                request.user,
                data['product_id'],
                data.get('quantity', 1),
            )
            totals = db_cart.cart_totals(request.user)
        else:
            session_cart.add_item(
                request.session,
                data['product_id'],
                data.get('quantity', 1),
            )
            totals = session_cart.cart_totals(request.session)
        return Response(_serialize_cart_payload(totals), status=201)


class CartItemView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, item_id: int):
        ser = CartItemPatchSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        qty = ser.validated_data['quantity']
        if request.user.is_authenticated:
            db_cart.set_quantity(request.user, item_id, qty)
            totals = db_cart.cart_totals(request.user)
        else:
            # item_id for session is not numeric PK — accept key via query? use product_id
            return Response(
                {'detail': 'Session cart: use product_id query params'},
                status=400,
            )
        return Response(_serialize_cart_payload(totals))

    def delete(self, request, item_id: int):
        if request.user.is_authenticated:
            db_cart.remove_item(request.user, item_id)
            totals = db_cart.cart_totals(request.user)
        else:
            return Response({'detail': 'Auth required for item id delete'}, status=400)
        return Response(_serialize_cart_payload(totals))


class CheckoutView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonCheckoutThrottle]

    def post(self, request):
        ser = CheckoutSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        if request.user.is_authenticated:
            totals = db_cart.cart_totals(request.user)
        else:
            totals = session_cart.cart_totals(request.session)
        if not totals['items']:
            return Response({'detail': 'Cart is empty'}, status=400)

        issues = totals.get('issues') or []
        if issues:
            return Response({'detail': 'Cart unavailable', 'issues': issues}, status=400)

        delivery_cost = data.get('delivery_cost') or Decimal('0')
        priced = convert_cart_totals(totals, delivery_cost)
        from apps.core.money import MIN_UNIT_PRICE, money, reconcile_order_totals
        if money(priced['total']) < MIN_UNIT_PRICE:
            return Response({'detail': 'Invalid order total'}, status=400)
        status_code = Order.STATUS_PENDING
        if data['payment_method'] == Order.PAYMENT_ONLINE:
            status_code = Order.STATUS_AWAITING_PAYMENT

        from apps.cart import stock as stock_svc

        with transaction.atomic():
            consume_issues = stock_svc.consume_for_checkout(
                totals['items'],
                session=request.session,
                user=request.user if request.user.is_authenticated else None,
            )
            if consume_issues:
                return Response(
                    {'detail': 'Cart unavailable', 'issues': consume_issues},
                    status=400,
                )
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                email=data['email'],
                comment=data.get('comment') or '',
                delivery_service=data['delivery_service'],
                delivery_city=data['delivery_city'],
                delivery_address=data['delivery_address'],
                np_city_ref=data.get('np_city_ref') or '',
                np_warehouse_ref=data.get('np_warehouse_ref') or '',
                payment_method=data['payment_method'],
                subtotal=money(priced['subtotal']),
                discount=money(0),
                delivery_cost=money(priced['delivery_cost']),
                total=money(priced['total']),
                currency=priced['currency'],
                fx_rate=priced['fx_rate'],
                status=status_code,
            )
            for item in priced['items']:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=str(item['product']),
                    product_sku=item['product'].sku or '',
                    price=money(item['unit_price']),
                    quantity=item['quantity'],
                    line_total=money(item['line_total']),
                )
            reconcile_order_totals(order)
            if request.user.is_authenticated:
                db_cart.clear(request.user)
            else:
                session_cart.clear(request.session)

        notify_order_created(order)
        payload = OrderDetailSerializer(order).data
        if order.payment_method == Order.PAYMENT_ONLINE:
            payload.update(pay_svc.online_payment_payload(request, order))
        return Response(payload, status=status.HTTP_201_CREATED)
