from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ En production, mets SECRET_KEY dans une variable d'environnement,
# jamais en clair dans le code versionné (git).
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-@x6q$t_7%n%ch)2qo!+!-6wf)7riv6=wi!@mf5ji-*rw2kalnu'  # valeur de secours pour le dev local uniquement
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    # =====================================================
    # ADMIN DJANGO
    # =====================================================
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # =====================================================
    # PACKAGES TIERS
    # =====================================================
    'widget_tweaks',
    'crispy_forms',
    'crispy_bootstrap5',
    # 'debug_toolbar',  # ⚠️ Désactivé : incompatible avec Django 6.1 (RecursionError sur staticfiles_storage.url())
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'simple_history',
    'django_countries',
    'corsheaders',

    # =====================================================
    # MODULES SANITA
    # =====================================================
    'accounts',
    'parametrage_general',
    'abonnement',
    'personnels',
    'patients',
    'consultations',
    'consultations_dentaires',
    'ordonnances',
    'medicaments',
    'stock',
    'laboratoires',
    'infirmiers',
    'pharmacie',
    'cliniques_partenaires',
    'documents',
    'administration',
    'dashboard',
    'api',
    'front',
    'medecins',
    'imagerie',
    'workflow',
    'cartes_sanitaires',
    'entreprises',

    # =====================================================
    # SYSTEME
    # =====================================================
    'notifications.apps.NotificationsConfig',
    'audit',
]

AUTH_USER_MODEL = 'accounts.CustomUser'

JAZZMIN_SETTINGS = {
    "site_title": "Interface d'administration",
    "site_header": "Administration SANITA",
    "site_brand": "SANITA",
    "welcome_sign": "Bienvenue dans l'administration du SANITA",
    "copyright": "© 2025 Ta Société",
    "search_model": "accounts.customuser",
    "user_avatar": "avatar",

    "topmenu_links": [
        {"name": "Accueil", "url": "/", "permissions": ["auth.view_user"]},
        {"model": "accounts.customuser"},
        {"app": "personnels"},
    ],

    "icons": {
        "accounts.customuser": "fas fa-user-tie",
        "auth.group": "fas fa-users",
        "personnels.employe": "fas fa-id-badge",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["accounts", "personnels", "parametrage_general"],
    "hide_models": ["auth.permission", "auth.group"],
    "related_modal_active": True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Nécessaire uniquement si debug_toolbar est réactivé un jour (version compatible avec Django 6.1 disponible)
# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

ROOT_URLCONF = 'sanita_project.urls'

SITE_DOMAIN = "localhost:8000"
PROTOCOL = "http"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'parametrage_general.context_processors.configuration_etablissement',
            ],
        },
    },
]

WSGI_APPLICATION = 'sanita_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'sanita_projet_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'; SET sql_mode='STRICT_TRANS_TABLES';",
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

ACCOUNT_EMAIL_MAX_LENGTH = 191

# Internationalization
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
    ('es', 'Español'),
    ('de', 'Deutsch'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------------------------------------
# 🔑 REDIRECTIONS LOGIN
# ----------------------------------------
from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy('accounts:admin_login')
LOGIN_REDIRECT_URL = reverse_lazy('dashboard:index')  # ✅ corrigé — 'parametrage_general:dashboard' n'existe pas

# ----------------------------------------
# 📧 EMAIL — à activer si besoin, jamais avec des identifiants en clair
# ----------------------------------------
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = f"SANITA <{os.environ.get('EMAIL_HOST_USER')}>"

# Notifications Settings
NOTIFICATIONS_USE_JSONFIELD = True

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

# ----------------------------------------
# 🌱 CELERY CONFIGURATION
# ----------------------------------------
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_TRACK_STARTED = True
CELERY_TIMEZONE = TIME_ZONE

# CSRF / Cookies
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# ✅ Secure=True bloque les cookies en HTTP (localhost).
#    Ne mets True qu'en production (HTTPS).
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

CSRF_USE_SESSIONS = False

# Avertissement MySQL non bloquant (contrainte unique conditionnelle sur allauth.EmailAddress)
SILENCED_SYSTEM_CHECKS = ["models.W036"]