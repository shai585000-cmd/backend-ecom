# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""

from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# backend/
APPS_DIR = BASE_DIR / "backend"
env = environ.Env()
environ.Env.read_env()


READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    env.read_env(str(BASE_DIR / ".env"))


DEBUG = env.bool("DJANGO_DEBUG", False)

TIME_ZONE = "GMT"
LANGUAGE_CODE = "en-us"

SITE_ID = 1
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(BASE_DIR / "locale")]



DATABASES = {"default": env.db("DATABASE_URL", default="postgresql://e_commerce_6c64_user:kahJ0huW9mo8LnCPemTsRLTkdkXm7CGT@dpg-d69c0n0gjchc73chbnk0-a.oregon-postgres.render.com/e_commerce_6c64")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# Application definition
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    'jazzmin',
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [

    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
]

LOCAL_APPS = [
    "backend.users",
    "backend.produits",
    "backend.cart",
    "backend.home",
    "backend.orders",
    "backend.payments",
    "backend.reviews",
    "backend.wishlist",
    "backend.shipping",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIGRATION_MODULES = {"sites": "backend.contrib.sites.migrations"}



AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = "users:redirect"

LOGIN_URL = "account_login"


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]




MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False  
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Configuration de la sécurité
CSRF_COOKIE_SECURE = False  # Mettre à True en production
SESSION_COOKIE_SECURE = False  # Mettre à True en production
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# Permettre l'envoi du cookie CSRF
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_NAME = 'csrftoken'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}



STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]



MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = "/media/"



TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "backend.users.context_processors.allauth_settings",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"


FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)



SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"


EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_TIMEOUT = 5

# ADMIN
ADMIN_URL = "admin/"
ADMINS = [("""OFFO ANGE EMMANUEL""", "offo-ange-emmanuel@example.com")]
MANAGERS = ADMINS

DJANGO_ADMIN_FORCE_ALLAUTH = env.bool("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_SSL = REDIS_URL.startswith("rediss://")



ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_ADAPTER = "backend.users.adapters.AccountAdapter"
ACCOUNT_FORMS = {"signup": "backend.users.forms.UserSignupForm"}
SOCIALACCOUNT_ADAPTER = "backend.users.adapters.SocialAccountAdapter"
SOCIALACCOUNT_FORMS = {"signup": "backend.users.forms.UserSocialSignupForm"}

# Configuration Google OAuth
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

# URL de redirection apres authentification Google
GOOGLE_OAUTH_CALLBACK_URL = env('GOOGLE_OAUTH_CALLBACK_URL', default='https://frontend-ecom-weld.vercel.app/')
SOCIALACCOUNT_LOGIN_ON_GET = True


CORS_URLS_REGEX = r"^/api/.*$"

SPECTACULAR_SETTINGS = {
    "TITLE": "backend API",
    "DESCRIPTION": "Documentation of API endpoints of backend",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "SCHEMA_PATH_PREFIX": "/api/",
}



SECRET_KEY = "django-insecure-votre-clé-secrète"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',
}


# Custom Admin Settings

JAZZMIN_SETTINGS = {
    "site_title": "TECHSTORE",
    "site_header": "TECHSTORE",
    "site_brand": "TECHSTORE",
    "site_logo": None,
    "login_logo": None,
    "site_logo_classes": "img-circle",
    
    "welcome_sign": "Bienvenue sur votre espace de gestion",
    "copyright": "TECHSTORE - Votre boutique en ligne",
    "user_avatar": None,
    
    # Liens du menu supérieur - simplifiés
    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "icon": "fas fa-home"},
        {"name": "Produits", "url": "admin:backend_produits_product_changelist", "icon": "fas fa-mobile-alt"},
        {"name": "Commandes", "url": "admin:backend_orders_order_changelist", "icon": "fas fa-shopping-cart"},
        {"name": "Voir le site", "url": "https://frontend-ecom-weld.vercel.app/", "new_window": True, "icon": "fas fa-external-link-alt"},
    ],
    
    "show_sidebar": True,
    "navigation_expanded": True,
    
    # Ordre des applications dans le menu - les plus importantes en premier
    "order_with_respect_to": [
        "produits",
        "orders",
        "home",
        "users",
        "reviews",
        "shipping",
    ],
    
    # Icônes claires et intuitives
    "icons": {
        "admin.LogEntry": "fas fa-history",
        
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        # Produits
        "produits": "fas fa-mobile-alt",
        "produits.Product": "fas fa-mobile-alt",
        "produits.Brand": "fas fa-tag",
        
        # Commandes
        "orders": "fas fa-shopping-cart",
        "orders.Order": "fas fa-shopping-cart",
        "orders.OrderItem": "fas fa-list",
        
        # Accueil/Site
        "home": "fas fa-home",
        "home.Banner": "fas fa-image",
        "home.Category": "fas fa-folder",
        "home.Announcement": "fas fa-bullhorn",
        
        # Utilisateurs
        "users": "fas fa-users",
        "users.User": "fas fa-user",
        
        # Avis
        "reviews": "fas fa-star",
        "reviews.Review": "fas fa-star",
        
        # Livraison
        "shipping": "fas fa-truck",
        "shipping.ShippingZone": "fas fa-map-marker-alt",
        
        # Panier
        "cart": "fas fa-shopping-basket",
        "cart.Cart": "fas fa-shopping-basket",
        
        # Wishlist
        "wishlist": "fas fa-heart",
        "wishlist.Wishlist": "fas fa-heart",
        
        # Paiements
        "payments": "fas fa-credit-card",
        "payments.Payment": "fas fa-credit-card",
    },
    
    "default_icon_parents": "fas fa-folder-open",
    "default_icon_children": "fas fa-circle",
    
    "related_modal_active": True,
    
    "custom_js": None,
    "show_ui_builder": False,  # Cacher pour le client
    
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
        "produits.product": "horizontal_tabs",
        "orders.order": "horizontal_tabs",
    },
    
    # Masquer certains modèles techniques pour le client
    "hide_apps": [],
    "hide_models": [
        "auth.Group",
        "socialaccount.SocialAccount",
        "socialaccount.SocialToken",
        "socialaccount.SocialApp",
        "account.EmailAddress",
        "sites.Site",
    ],
    
    # Personnalisation des noms d'apps pour plus de clarté
    "custom_links": {},
    
    # Recherche globale
    "search_model": ["produits.Product", "orders.Order", "users.User"],
}





# Jazzmin Tweaks

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-indigo",
    "accent": "accent-olive",
    "navbar": "navbar-indigo navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "custom_css": "admin/css/custom.css",
}


