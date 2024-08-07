from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    class Meta:
        permissions = [
            ("is_admin", "Can manage administration"),
            ("is_teacher", "Can manage teachers")
        ]
