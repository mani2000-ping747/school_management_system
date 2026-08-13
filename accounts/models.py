from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("PRINCIPAL", "Principal"),
        ("ACCOUNTANT", "Accountant"),
        ("TEACHER", "Teacher"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="ACCOUNTANT")

    mobile = models.CharField(max_length=15, blank=True, null=True)

    profile_image = models.ImageField(upload_to="users/", blank=True, null=True)

    def __str__(self):
        return self.username
