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

    # Jazzmin must come before Django admin
    'jazzmin',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
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

    # Custom activity tracking
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
        'ENGINE':
            'django.db.backends.sqlite3',

        'NAME':
            BASE_DIR / 'db.sqlite3',
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
# JAZZMIN ADMIN CONFIGURATION
# ============================================================

JAZZMIN_SETTINGS = {

    # ========================================================
    # BRANDING
    # ========================================================

    "site_title": "Mahashankh Admin",

    "site_header": "Mahashankh Admin Panel",

    "site_brand": "Mahashankh Wallpapers",

    "welcome_sign": "Welcome to Mahashankh Admin Dashboard",

    "copyright": "Mahashankh Design & Technology",

    # Correct Static Paths
    "custom_css": "admin/css/mahashankh.css",
    "custom_js": "admin/js/mahashankh-theme.js",  

    "site_logo": None, 
    "login_logo": None,


    # ========================================================
    # SIDEBAR
    # ========================================================

    "show_sidebar":
        True,

    "navigation_expanded":
        True,


    # ========================================================
    # HIDE UNNECESSARY MODELS
    # ========================================================

    # Village is not required in the visible admin sidebar
    "hide_models": [

        "dashboard.areavillage",
    ],


    "hide_apps": [],


    # ========================================================
    # PROPER ADMIN MENU ORDER
    # ========================================================

    "order_with_respect_to": [

        # -------------------------------
        # MAIN
        # -------------------------------

        "dashboard",


        # -------------------------------
        # WALLPAPER MANAGEMENT
        # -------------------------------

        "dashboard.category",

        "dashboard.wallpaper",


        # -------------------------------
        # USER MANAGEMENT
        # -------------------------------

        "auth.user",

        "dashboard.userprofile",

        "dashboard.useractivitylog",


        # -------------------------------
        # AI MANAGEMENT
        # -------------------------------

        "dashboard.aigeneration",

        "dashboard.generatedimage",


        # -------------------------------
        # CHAT MANAGEMENT
        # -------------------------------

        "dashboard.chatsession",

        "dashboard.chatbotlog",


        # -------------------------------
        # COMMERCE
        # -------------------------------

        "dashboard.product",

        "dashboard.order",


        # -------------------------------
        # SYSTEM
        # -------------------------------

        "dashboard.permissionrecord",

        "auth.group",
    ],


    # ========================================================
    # ADMIN ICONS
    # ========================================================

    "icons": {

        # Dashboard
        "dashboard":
            "fas fa-chart-pie",


        # Wallpaper Management
        "dashboard.category":
            "fas fa-layer-group",

        "dashboard.wallpaper":
            "fas fa-images",


        # User Management
        "auth.user":
            "fas fa-users",

        "dashboard.userprofile":
            "fas fa-user-circle",

        "dashboard.useractivitylog":
            "fas fa-user-clock",


        # AI Management
        "dashboard.aigeneration":
            "fas fa-robot",

        "dashboard.generatedimage":
            "fas fa-wand-magic-sparkles",


        # Chat
        "dashboard.chatsession":
            "fas fa-comments",

        "dashboard.chatbotlog":
            "fas fa-comment-dots",


        # Commerce
        "dashboard.product":
            "fas fa-box",

        "dashboard.order":
            "fas fa-shopping-cart",


        # System
        "dashboard.permissionrecord":
            "fas fa-shield-halved",

        "auth.group":
            "fas fa-user-shield",
    },


    # ========================================================
    # CUSTOM CSS
    # ========================================================

    "custom_css":
        "admin/css/mahashankh.css",


    # ========================================================
    # UI BUILDER
    # ========================================================

    "show_ui_builder":
        False,
}


# ============================================================
# JAZZMIN UI SETTINGS
# ============================================================



JAZZMIN_UI_TWEAKS = {
    "theme": "default", 
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-warning",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
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


# ============================================================
# STORAGE
# ============================================================

STORAGES = {

    "default": {
        "BACKEND":
            "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND":
            "whitenoise.storage.CompressedStaticFilesStorage",
    },
}