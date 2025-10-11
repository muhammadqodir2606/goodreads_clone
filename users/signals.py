from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser
from users.tasks import send_email


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_email.delay(
            "Welcome to my website",
            f"Hello {instance.username}! Welcome to my website",
            [instance.email]
        )
