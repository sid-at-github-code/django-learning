
# bookings/models.py
from django.db import models
from accounts.models import User

class Order(models.Model):
    STATUS_CHOICES = (
        ('started', 'Started'),
        ('reached', 'Reached'),
        ('collected', 'Collected'),
        ('delivered', 'Delivered'),
    )

    customer = models.ForeignKey(User, related_name='customer_orders', on_delete=models.CASCADE)
    delivery = models.ForeignKey(User, related_name='delivery_orders', on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField(blank=True)  # order details (simple text)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='started')
    chat_enabled = models.BooleanField(default=False)  # enabled after handler assigns delivery guy
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.phone} - {self.status}"
