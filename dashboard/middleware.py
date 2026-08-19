from django.utils.deprecation import MiddlewareMixin

from .models import UserActivityLog


class UserActivityMiddleware(MiddlewareMixin):
    """
    Tracks logged-in user activity and IP address.
    """

    def process_request(self, request):

        if not request.user.is_authenticated:
            return None

        # Ignore admin static/media requests
        if request.path.startswith('/static/'):
            return None

        if request.path.startswith('/media/'):
            return None

        # Get user IP
        ip_address = request.META.get(
            'HTTP_X_FORWARDED_FOR'
        )

        if ip_address:
            ip_address = ip_address.split(',')[0].strip()
        else:
            ip_address = request.META.get(
                'REMOTE_ADDR'
            )

        # Avoid creating activity for every admin page request
        # repeatedly.
        important_paths = (
            '/admin/login/',
            '/admin/logout/',
        )

        if request.path in important_paths:
            return None

        # Only track meaningful admin/user activity
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):

            UserActivityLog.objects.create(
                username=request.user.username,
                action=f"{request.method} {request.path}",
                ip_address=ip_address,
            )

        return None