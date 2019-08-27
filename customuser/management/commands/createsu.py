from django.core.management.base import BaseCommand
from customuser.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if (User.objects.filter(email='admin@admin.com').count() == 0):
            User.objects.create_superuser("admin@admin.com", "admin")