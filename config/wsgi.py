"""
WSGI config for AmmHelpDesk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import sys
sys.path.append("C:/Apache24/htdocs/AMMHelpDesk")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

application = get_wsgi_application()
