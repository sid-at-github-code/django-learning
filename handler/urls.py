# handler/urls.py
from django.urls import path
from . import views

app_name = 'handler'

urlpatterns = [
    path('all/', views.all_bookings, name='all_bookings'),
    path('assign/<int:order_id>/', views.assign_booking, name='assign_booking'),
]
