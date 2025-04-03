from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),

    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ADMIN)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
