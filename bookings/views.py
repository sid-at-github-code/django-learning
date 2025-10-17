# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from accounts.models import User

# Helper: get current user from session (simple)
def get_current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

# Customer: create order
def create_order(request):
    user = get_current_user(request)
    if not user or user.role != 'customer':
        return redirect('accounts:login')

    if request.method == 'POST':
        details = request.POST.get('details', '').strip()
        Order.objects.create(customer=user, details=details, status='started', chat_enabled=False)
        return redirect('bookings:list_orders')

    return render(request, 'bookings/create_order.html', {'user': user})

# List orders: behavior depends on role
def list_orders(request):
    user = get_current_user(request)
    if not user:
        return redirect('accounts:login')

    if user.role == 'customer':
        orders = Order.objects.filter(customer=user).order_by('-created_at')
        return render(request, 'bookings/list_orders.html', {'orders': orders, 'user': user})
    elif user.role == 'delivery':
        return redirect('bookings:delivery_orders')
    elif user.role == 'admin':
        return redirect('handler:all_bookings')
# Order detail / update status (delivery guy updates status)
def order_detail(request, order_id):
    user = get_current_user(request)
    if not user:
        return redirect('accounts:login')

    order = get_object_or_404(Order, id=order_id)

    # Only assigned delivery guy can update status, or customer/admin can view
    can_update = (user.role == 'delivery' and order.delivery and order.delivery.id == user.id)

    if request.method == 'POST' and can_update:
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            # If delivered, disable chat
            if new_status == 'delivered':
                order.chat_enabled = False
            order.save()
        return redirect('bookings:order_detail', order_id=order.id)

    # pass status choices for template iteration
    status_choices = Order.STATUS_CHOICES

    return render(request, 'bookings/order_detail.html', {
        'order': order,
        'can_update': can_update,
        'status_choices': status_choices,
        'user': user,
    })

# Delivery: view only assigned orders
def delivery_orders(request):
    user = get_current_user(request)
    if not user or user.role != 'delivery':
        return redirect('accounts:login')

    orders = Order.objects.filter(delivery=user).order_by('-created_at')
    return render(request, 'bookings/delivery_orders.html', {'orders': orders, 'user': user})
