from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("member", "Member"),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_staff = True
        elif self.role == "admin":
            self.is_staff = True
        else:
            self.is_staff = False
        
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == "admin"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
