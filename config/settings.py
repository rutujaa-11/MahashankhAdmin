import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = 'django-insecure-your-secret-key-here'


DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
]


# ============================================================
# INSTALLED APPS
# ============================================================

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'dashboard',
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'dashboard.middleware.UserActivityMiddleware',
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = 'config.urls'


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        'BACKEND':
            'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.debug',

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'dashboard.context_processors.admin_dashboard_data',
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = 'config.wsgi.application'


# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator',
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# JAZZMIN CONFIGURATION
# ============================================================

JAZZMIN_SETTINGS = {

    "site_title":
        "Wallpaper Admin",

    "site_header":
        "Wallpaper Panel",

    "site_brand":
        "Mahashankh Wallpapers",

    "welcome_sign":
        "Welcome to Wallpaper Admin Dashboard",

    "copyright":
        "Mahashankh Ltd",

    "show_sidebar":
        True,

    "navigation_expanded":
        True,

    "hide_apps":
        [],

    "hide_models":
        [],

    "order_with_respect_to":
        [
            "dashboard",
            "auth",
        ],

    "icons": {

        "dashboard":
            "fas fa-chart-line",

        "dashboard.category":
            "fas fa-layer-group",

        "dashboard.wallpaper":
            "fas fa-images",

        "dashboard.useractivitylog":
            "fas fa-user-clock",

        "auth.user":
            "fas fa-users",

        "auth.group":
            "fas fa-user-shield",
    },

    "custom_css":
        "admin/css/mahashankh.css",

    "show_ui_builder":
        False,
}


# ============================================================
# JAZZMIN UI SETTINGS
# ============================================================

JAZZMIN_UI_TWEAKS = {

    "theme":
        "flatly",

    "navbar_small_text":
        False,

    "footer_small_text":
        False,

    "body_small_text":
        False,

    "brand_small_text":
        False,

    "brand_colour":
        "navbar-white",

    "accent":
        "accent-brown",

    "navbar":
        "navbar-white",

    "no_navbar_border":
        False,

    "sidebar":
        "sidebar-light-brown",

    "sidebar_nav_small_text":
        False,

    "sidebar_disable_expand":
        False,

    "sidebar_nav_child_indent":
        True,

    "sidebar_nav_compact_style":
        False,

    "sidebar_nav_legacy_style":
        False,

    "sidebar_nav_flat_style":
        True,

    "button_classes": {

        "primary":
            "btn-outline-brown",

        "secondary":
            "btn-outline-secondary",

        "info":
            "btn-outline-info",

        "warning":
            "btn-outline-warning",

        "danger":
            "btn-outline-danger",

        "success":
            "btn-outline-success",
    },
}


# ============================================================
# LOGIN
# ============================================================

LOGIN_REDIRECT_URL = '/admin/'

LOGIN_URL = '/'


# ============================================================
# SESSION
# ============================================================

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7

SESSION_SAVE_EVERY_REQUEST = True