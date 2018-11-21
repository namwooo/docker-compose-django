from .base import *

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'handys',
        'USER': 'poet',
        'PASSWORD': 'demian!89',
        'HOST': 'localhost',
        'PORT': '',
    }
}
