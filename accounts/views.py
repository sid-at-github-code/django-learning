
# accounts/views.py

from django.shortcuts import render, redirect
from .models import User

# Signup page
def signup(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        role = request.POST['role']
        otp = request.POST['otp']
        if otp == '1234':  # dummy OTP as mentionaed for assignment in mail
            User.objects.create(phone=phone, password=password, role=role)
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Invalid OTP'})
    return render(request, 'accounts/signup.html')

# Login page
# accounts/views.py snippet
def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            user = User.objects.get(phone=phone, password=password)
            # Login successful
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            # Redirect based on role
            if user.role == 'admin':
                return redirect('handler:all_bookings')
            elif user.role == 'customer':
                return redirect('bookings:list_orders')
            elif user.role == 'delivery':
                return redirect('bookings:delivery_orders')  # THIS WAS MISSING
        except User.DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')
