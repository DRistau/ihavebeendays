from .base import *


DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
