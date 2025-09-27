from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    image = models.ImageField(
        default='default.jpg',
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'png', 'jpg', 'jpeg', 'heic'
                ]
            )
        ]
    )
