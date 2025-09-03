"""
Django settings for djcore project.
"""

import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Caricamento Variabili d'Ambiente ---
ENV_FILE = BASE_DIR.parent / ".env"
env = environ.Env()

if ENV_FILE.exists():
    environ.Env.read_env(str(ENV_FILE))
else:
    print("Nessun file .env trovato.")

# --- Impostazioni di Sicurezza e Core ---
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

if not DEBUG:
    ALLOWED_HOSTS.append('.ondigitalocean.app')

# --- Definizione delle Applicazioni ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'declaration_app',
    'anagrafica',
    'django_vite',
    'corsheaders',
    'riepilogo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # QUI: Aggiunto il middleware di WhiteNoise. La posizione è importante.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'djcore.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'djcore.wsgi.application'

# --- Database ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Validazione Password ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internazionalizzazione ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Gestione File Statici e Integrazione Vite ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR.parent / "frontend/dist",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# QUI: Aggiunta la configurazione per lo storage di WhiteNoise
# Questo ottimizza il modo in cui i file vengono serviti.
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

VITE_MANIFEST_PATH = BASE_DIR / "frontend/dist/manifest.json"
if not DEBUG:
    VITE_MANIFEST_PATH = STATIC_ROOT / "manifest.json"

DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "manifest_path": VITE_MANIFEST_PATH,
        "dev_server_host": "127.0.0.1",
        "dev_server_port": 5173,
    }
}

# --- URL di Autenticazione ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

