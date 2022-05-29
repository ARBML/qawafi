"""
Django settings for qawafi_server project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# import sys

# add base dir parent to path to include bohour package
# sys.path.append(f"{BASE_DIR}/..")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ufma(6oiywi6lused#m%nfg7nx#3q8d=&4$4ojr_ittmvml+9v"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "qawafi_server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "qawafi_server.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DIACRITIZER_HOST_URL = "http://172.18.0.22:8080"
# DIACRITIZER_HOST_URL = "http://127.0.0.1:8080"
DIACRITIZER_HOST_URL = "http://host.docker.internal:8080"

# meters related

import glob

BOHOUR_NAMES = [
    "saree",
    "kamel",
    "mutakareb",
    "mutadarak",
    "munsareh",
    "madeed",
    "mujtath",
    "ramal",
    "baseet",
    "khafeef",
    "taweel",
    "wafer",
    "hazaj",
    "rajaz",
    "mudhare",
    "muqtatheb",
    "nathr",
]
BOHOUR_NAMES_AR = [
    "السريع",
    "الكامل",
    "المتقارب",
    "المتدارك",
    "المنسرح",
    "المديد",
    "المجتث",
    "الرمل",
    "البسيط",
    "الخفيف",
    "الطويل",
    "الوافر",
    "الهزج",
    "الرجز",
    "المضارع",
    "المقتضب",
    "نثر",
]

BOHOUR_PATTERNS = {}
for bahr_file in glob.glob("./bohour_patterns/ints/*.txt"):
    patterns = open(bahr_file, "r").read().splitlines()
    bahr_name = bahr_file.split("/")[-1].split(".")[0]
    if bahr_name not in BOHOUR_NAMES:
        # print(bahr_name)
        continue
    BOHOUR_PATTERNS[bahr_name] = patterns

BOHOUR_TAFEELAT = {}
for bahr_file in glob.glob("./bohour_patterns/strs/*.txt"):
    patterns = open(bahr_file, "r").read().splitlines()
    bahr_name = bahr_file.split("/")[-1].split(".")[0]
    if bahr_name not in BOHOUR_NAMES:
        # print(bahr_name)
        continue
    BOHOUR_TAFEELAT[bahr_name] = patterns

# get the model
print("trying loading the meters model")
from .meters import create_transformer_model, create_model_v1, create_era_theme_model


METERS_MODEL = create_transformer_model()
METERS_MODEL.load_weights("./deep-learning-models/meters_model/cp.ckpt")

# get the embeddings model
BASE_MODEL = create_model_v1()
BASE_MODEL.load_weights("./deep-learning-models/embeddings_extractor_model/cp.ckpt")

from tensorflow.keras.models import Model

FEATURES_EXTRACTOR = Model(BASE_MODEL.layers[0].input, BASE_MODEL.layers[4].output)

from datasets import load_from_disk

BAITS_EMBEDDINGS = load_from_disk("./deep-learning-models/baits_embeddings")


import tkseem as tk

ERA_MODEL = create_era_theme_model()
ERA_MODEL.load_weights("./deep-learning-models/era_classification_model/cp.ckpt")

ERA_TOKENIZER = tk.SentencePieceTokenizer()
ERA_TOKENIZER.load_model("./deep-learning-models/era_classification_model/vocab.model")


THEME_MODEL = create_era_theme_model()
THEME_MODEL.load_weights("./deep-learning-models/theme_classification_model/cp.ckpt")

THEME_TOKENIZER = tk.SentencePieceTokenizer()
THEME_TOKENIZER.load_model(
    "./deep-learning-models/theme_classification_model/vocab.model"
)
