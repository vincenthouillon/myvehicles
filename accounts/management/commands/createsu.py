from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True):
            User.objects.create_superuser(  # type:ignore
                username=settings.SUPER_USER["username"],
                password=settings.SUPER_USER["password"],
            )
