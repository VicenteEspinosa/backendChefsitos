from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import User
class Command(BaseCommand):
    help = "DEV COMMAND: Fill database with initial data"

    def handle(self, *args, **options):
        call_command('loaddata','measurements')
        call_command('loaddata','users')
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()