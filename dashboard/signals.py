from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .models import UserActivityLog


# ============================================================
# USER ACCOUNT CREATED
# ============================================================

@receiver(post_save, sender=User)
def create_user_activity(sender, created, instance, **kwargs):

    if created:

        UserActivityLog.objects.create(
            username=instance.username,
            action="User Account Created"
        )


# ============================================================
# GET CLIENT IP
# ============================================================

def get_client_ip(request):

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


# ============================================================
# USER LOGIN
# ============================================================

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):

    UserActivityLog.objects.create(
        username=user.username,
        action="User Login",
        ip_address=get_client_ip(request)
    )


# ============================================================
# USER LOGOUT
# ============================================================

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):

    if user:

        UserActivityLog.objects.create(
            username=user.username,
            action="User Logout",
            ip_address=get_client_ip(request)
        )