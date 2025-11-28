# ruff: noqa: E501
"""
Settings for PythonAnywhere deployment.
"""
from .base import *  # noqa: F403
from .base import DATABASES
from .base import env
from .base import BASE_DIR

# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY", default="change-me-in-production")
DEBUG = env.bool("DJANGO_DEBUG", default=False)

# Remplacez 'votre-username' par votre nom d'utilisateur PythonAnywhere
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[
    "votre-username.pythonanywhere.com",
    "localhost",
    "127.0.0.1",
])

# DATABASE - PythonAnywhere supporte MySQL (gratuit) ou PostgreSQL (payant)
# Pour le plan gratuit, utilisez MySQL ou SQLite
# Option 1: SQLite (simple, pour commencer)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Option 2: MySQL (décommentez si vous utilisez MySQL sur PythonAnywhere)
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "votre-username$default",  # Format: username$dbname
#         "USER": "votre-username",
#         "PASSWORD": env("MYSQL_PASSWORD", default=""),
#         "HOST": "votre-username.mysql.pythonanywhere-services.com",
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# CACHES - Utiliser le cache local (pas de Redis sur PythonAnywhere gratuit)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# SECURITY
# ------------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False  # PythonAnywhere gère le SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# STATIC & MEDIA FILES
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# EMAIL - Console backend pour le développement/test
# Remplacez par un vrai service SMTP en production
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

# CORS - Ajoutez votre frontend URL
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Ajoutez votre URL frontend déployé ici
])

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[
    "https://votre-username.pythonanywhere.com",
])

# ADMIN
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")

# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(message)s",
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
