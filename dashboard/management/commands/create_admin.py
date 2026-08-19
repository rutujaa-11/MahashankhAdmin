from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the Django superuser"

    def handle(self, *args, **options):
        User = get_user_model()

        username = "admin"
        email = "admin@mahashankh.com"
        password = "Admin@12345"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user '{username}' created successfully."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user '{username}' updated successfully."
                )
            )