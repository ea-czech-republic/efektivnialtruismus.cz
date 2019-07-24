import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = False if os.environ.get("DEBUG") == "False" else True
INTERNAL_IPS = ["127.0.0.1"]
SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    "home",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.contrib.modeladmin",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "disqus",
    "wagtailmenus",
    "theses",
    "theses.tblog",
]
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar", "django_extensions"]


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

if DEBUG:
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

ROOT_URLCONF = "eacr.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtailmenus.context_processors.wagtailmenus",
            ]
        },
    }
]

WSGI_APPLICATION = "eacr.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            os.path.dirname(BASE_DIR),
            os.environ.get("DB_NAME", "dev-eacr.sqlite3"),
        ),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = (("en", "English"), ("cs", "Czech"))

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "static")]

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
MEDIA_URL = "/media/"

# Wagtail settings
WAGTAIL_SITE_NAME = os.environ.get("WAGTAIL_SITE_NAME", "efektivni-altruismus.cz")

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = "http://efektivni-altruismus.cz"

### THIS IS THE DEV/PROD part
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split()
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "c56q&sgquclsvweoixk^yof7o0f=$ebv7%jlqt_uupm_6pkr2@"
)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", None)
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)

DISQUS_WEBSITE_SHORTNAME = "efektivni-altruismus"
DISQUS_API_KEY = os.environ.get("DISQUS_API_KEY", "rubish")

DEFAULT_FROM_EMAIL = "no-reply@efektivni-altruismus.cz"
