from .base import *

Env = 'Dev'

TEST = True
DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

INTERNAL_IPS = [
    '127.0.0.1',
]
