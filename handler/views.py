
# handler/views.py
from django.shortcuts import render, redirect, get_object_or_404
from bookings.models import Order
from accounts.models import User

# Simple session-based current user helper (same pattern used in other apps)
def get_current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

# Admin / handler: view all orders
def all_bookings(request):
    user = get_current_user(request)
    if not user or user.role != 'admin':
        return redirect('accounts:login')

    orders = Order.objects.order_by('-created_at')
    return render(request, 'handler/all_bookings.html', {'orders': orders})

# Admin / handler: assign a delivery guy to an order
def assign_booking(request, order_id):
    user = get_current_user(request)
    if not user or user.role != 'admin':
        return redirect('accounts:login')

    order = get_object_or_404(Order, id=order_id)
    delivery_guys = User.objects.filter(role='delivery')

    # If already assigned, lock assignment permanently
    if order.delivery is not None:
        return render(request, 'handler/assign_booking.html', {
            'order': order,
            'delivery_guys': delivery_guys,
            'error': 'Delivery partner already assigned. Assignment is locked.'
        })

    if request.method == 'POST':
        delivery_id = request.POST.get('delivery_id')
        if delivery_id:
            try:
                delivery = User.objects.get(id=delivery_id, role='delivery')
                order.delivery = delivery
                order.chat_enabled = True
                order.save()
                return redirect('handler:all_bookings')
            except User.DoesNotExist:
                # invalid selection, fall through to template with error
                return render(request, 'handler/assign_booking.html', {
                    'order': order,
                    'delivery_guys': delivery_guys,
                    'error': 'Selected delivery user not found.'
                })

    return render(request, 'handler/assign_booking.html', {
        'order': order,
        'delivery_guys': delivery_guys
    })
