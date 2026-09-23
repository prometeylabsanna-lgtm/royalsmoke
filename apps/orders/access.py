"""Order access control (IDOR protection for authenticated orders)."""

from __future__ import annotations

ORDER_ACCESS_KEY = 'rs_order_access'
ORDER_ACCESS_MAX = 30


def grant_order_access(session, order_number: str) -> None:
    if not order_number:
        return
    nums = [n for n in (session.get(ORDER_ACCESS_KEY) or []) if n]
    if order_number not in nums:
        nums.append(order_number)
        session[ORDER_ACCESS_KEY] = nums[-ORDER_ACCESS_MAX:]
        session.modified = True


def can_view_order(request, order) -> bool:
    """Guest orders: order_number is enough. Auth orders: owner or same session."""
    if getattr(order, 'user_id', None) is None:
        return True
    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated and user.id == order.user_id:
        return True
    access = request.session.get(ORDER_ACCESS_KEY) or []
    if order.order_number in access:
        return True
    if request.session.get('rs_last_order') == order.order_number:
        return True
    return False
