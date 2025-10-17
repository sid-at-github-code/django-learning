
# accounts/models.py

from django.db import models

class User(models.Model):
    
    #admin is truely one but jsut for sake ,,
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('delivery', 'Delivery Guy'),
        ('admin', 'Admin'),
    )

    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)  # store hashed in real projects
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.phone} ({self.role})"
