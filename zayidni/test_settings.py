from .settings import *

# Use in-memory sqlite for tests to avoid external Postgres dependency
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Keep other settings from base
