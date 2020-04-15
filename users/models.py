from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Customer(models.Model):
    ROLE_CHOICES = [
        ('spad', 'superadmin'),
        ('ad', 'admin'),
        ('cus', 'customer')
    ]
    STATUS_CHOICES = [
        ('act', 'active'),
        ('pend', 'pending'),
        ('blk', 'blocked')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=4,
        choices=ROLE_CHOICES,
        default='cus',
    )
    status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default='act',
    )
