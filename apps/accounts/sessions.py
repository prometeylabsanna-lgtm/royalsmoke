"""Auth session helpers: flush other devices, keep cart as guest."""

from __future__ import annotations

from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.db import DatabaseError

from apps.cart import services as session_cart
from apps.cart.services import CART_SESSION_KEY


def snapshot_session_cart(session) -> dict:
    cart = session.get(CART_SESSION_KEY)
    return dict(cart) if isinstance(cart, dict) else {}


def restore_session_cart(session, cart: dict) -> None:
    session[CART_SESSION_KEY] = cart if isinstance(cart, dict) else {}
    session.modified = True


def flush_user_sessions(user, *, keep_session_key: str | None = None) -> int:
    """Delete all Django sessions belonging to user except optional current key."""
    deleted = 0
    uid = str(user.pk)
    for row in Session.objects.iterator():
        if keep_session_key and row.session_key == keep_session_key:
            continue
        try:
            data = row.get_decoded()
        except Exception:
            continue
        if str(data.get('_auth_user_id') or '') == uid:
            row.delete()
            deleted += 1
    return deleted


def logout_keeping_cart(request) -> None:
    """Log out but preserve session cart as guest cart."""
    from apps.cart import db_services as db_cart

    cart = snapshot_session_cart(request.session)
    user = getattr(request, 'user', None)
    if user is not None and getattr(user, 'is_authenticated', False):
        try:
            totals = db_cart.cart_totals(user)
            if totals.get('count'):
                session_cart.replace_raw(
                    request.session,
                    [
                        {'product_id': i['product'].id, 'qty': i['quantity']}
                        for i in totals['items']
                    ],
                )
                cart = snapshot_session_cart(request.session)
        except (DatabaseError, TypeError, AttributeError, KeyError):
            pass

    access = list(request.session.get('rs_order_access') or [])
    last_order = request.session.get('rs_last_order')
    logout(request)
    restore_session_cart(request.session, cart)
    if access:
        request.session['rs_order_access'] = access
    if last_order:
        request.session['rs_last_order'] = last_order
    request.session.modified = True


def delete_account_to_guest(request, user) -> None:
    """Delete user account; current browser stays guest with cart."""
    from apps.cart import db_services as db_cart

    cart = snapshot_session_cart(request.session)
    try:
        totals = db_cart.cart_totals(user)
        if totals.get('count'):
            session_cart.replace_raw(
                request.session,
                [
                    {'product_id': i['product'].id, 'qty': i['quantity']}
                    for i in totals['items']
                ],
            )
            cart = snapshot_session_cart(request.session)
    except (DatabaseError, TypeError, AttributeError, KeyError):
        pass

    flush_user_sessions(user, keep_session_key=None)
    user.delete()
    request.session.flush()
    restore_session_cart(request.session, cart)
