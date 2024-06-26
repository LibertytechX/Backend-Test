from .base import *

SECRET_KEY = '92yc9A4oOY%~?6\n]&xZc6+mW)"8)KMMZ8&KbSC\|gIPX!<[RQ9Co-4W_A#PsiG'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'libertydb',
#         'USER': 'liberty',
#         'PASSWORD': 'liberty',
#         'HOST': 'localhost',  
#         'PORT': '5432',      
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

