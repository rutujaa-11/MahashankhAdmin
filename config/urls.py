from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # ========================================================
    # ROOT → ADMIN
    # ========================================================

    path(
        '',
        lambda request: redirect('/admin/')
    ),

    # ========================================================
    # DJANGO ADMIN
    # ========================================================

    path(
        'admin/',
        admin.site.urls
    ),

]


# ============================================================
# MEDIA FILES
# ============================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )