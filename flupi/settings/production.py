from .base import *
from dotenv import load_dotenv
from ..logging import *

# Cargamos las variables de entorno
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles')

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}