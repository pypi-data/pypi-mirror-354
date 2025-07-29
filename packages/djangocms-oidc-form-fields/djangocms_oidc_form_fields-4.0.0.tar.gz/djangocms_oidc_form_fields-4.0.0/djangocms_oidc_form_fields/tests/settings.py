SECRET_KEY = "secret"

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Django CMS
    'cms',
    'menus',
    'treebeard',
    'sekizai',
    'easy_thumbnails',
    'djangocms_alias',
    # dependencies
    'mozilla_django_oidc',
    'filer',
    'aldryn_forms',
    # the project
    'djangocms_oidc',
    'django_countries',
    'djangocms_oidc_form_fields',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'djangocms_oidc.auth.DjangocmsOIDCAuthenticationBackend',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["djangocms_oidc_form_fields/tests/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

CMS_TEMPLATES = (
    ('test_page.html', 'Normal page'),
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "tests",
    }
}

TIME_ZONE = "UTC"
USE_TZ = True

LANGUAGE_CODE = "en"
LANGUAGES = [
    ('en', 'English'),
]

CMS_CONFIRM_VERSION4 = True
SITE_ID = 1
ROOT_URLCONF = 'djangocms_oidc_form_fields.tests.urls'
STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
