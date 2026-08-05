"""Create or update the admin account: python manage.py ensure_admin

Django's built-in `createsuperuser --noinput` refuses to run if the user
already exists, which makes it useless on a platform that restarts the
container on every deploy.

This command is IDEMPOTENT: run it once or a hundred times, the result is
the same -- an admin account exists with the password from the environment.
That property is what makes it safe to put in a startup command.
"""

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ensure a superuser exists with the password from the environment"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write("DJANGO_SUPERUSER_USERNAME/PASSWORD not set -- skipping.")
            return

        user, created = User.objects.get_or_create(
            username=username, defaults={"email": email}
        )
        # set_password HASHES it. Assigning user.password directly would store
        # the raw text and make every login fail.
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"admin '{username}' {'created' if created else 'password reset'}"
            )
        )
