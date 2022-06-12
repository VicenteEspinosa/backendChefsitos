from django.contrib.auth.models import User
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "DEV COMMAND: Fill database with initial data"

    def handle(self, *args, **options):
        call_command("loaddata", "ingredients")
        call_command("loaddata", "measurements")
        call_command("loaddata", "tags")
        call_command("loaddata", "users")
        call_command("loaddata", "recipes")
        call_command("loaddata", "recipe_ingredient_measurement")
        call_command("loaddata", "items")
        call_command("loaddata", "recipe_tag")
        call_command("loaddata", "ratings")
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
