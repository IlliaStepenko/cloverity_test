from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create user for demo"

    def handle(self, *args, **options):
        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=settings.DEMO_USER_EMAIL,
            email=settings.DEMO_USER_EMAIL,
            is_staff=False,
            is_superuser=False
        )

        if created:
            user.set_password(settings.DEMO_USER_PASSWORD)
            user.save()
