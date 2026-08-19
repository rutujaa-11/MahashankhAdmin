from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # http://127.0.0.1:8000/
    # automatically opens /admin/
    path(
        '',
        RedirectView.as_view(
            url='/admin/',
            permanent=False
        ),
    ),

    # http://127.0.0.1:8000/admin/
    path(
        'admin/',
        admin.site.urls
    ),

]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )