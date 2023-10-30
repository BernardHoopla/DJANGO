# myproject/settings.py
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Add 'myapp' to the list of installed apps
INSTALLED_APPS = [
    'example',
]

# Define the login URL
LOGIN_URL = 'login'


# POSTGRES_URL="postgres://default:7scq9ZVzkjGh@ep-round-union-02252091-pooler.us-east-1.postgres.vercel-storage.com:5432/verceldb"
# POSTGRES_PRISMA_URL="postgres://default:7scq9ZVzkjGh@ep-round-union-02252091-pooler.us-east-1.postgres.vercel-storage.com:5432/verceldb?pgbouncer=true&connect_timeout=15"
# POSTGRES_URL_NON_POOLING="postgres://default:7scq9ZVzkjGh@ep-round-union-02252091.us-east-1.postgres.vercel-storage.com:5432/verceldb"
# POSTGRES_USER="default"
# POSTGRES_HOST="ep-round-union-02252091-pooler.us-east-1.postgres.vercel-storage.com"
# POSTGRES_PASSWORD="7scq9ZVzkjGh"
# POSTGRES_DATABASE="verceldb"
#
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "verceldb",
        "USER": "default",
        "PASSWORD": "7scq9ZVzkjGh",
        "HOST": "ep-round-union-02252091-pooler.us-east-1.postgres.vercel-storage.com",
        "PORT": "5432",
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


print(BASE_DIR)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3'
#     }
# }

# Configure authentication backends and middleware (if not already done)
# ...

# Add a suitable template directory to TEMPLATE_DIRS
# ...

