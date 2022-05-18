from django.contrib.auth.models import User
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "DEV COMMAND: Fill database with initial data"

    def handle(self, *args, **options):
        call_command("loaddata", "measurements")
        call_command("loaddata", "users")
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
