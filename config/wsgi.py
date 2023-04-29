"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# application = get_wsgi_application()
import os
import django
import socketio

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.setting.base')

django.setup()

# sio = socketio.Server(async_mode='threading')

from apps.analysis.socket_handlers import sio
app = socketio.WSGIApp(sio)

# sio.WSGIApp(socket_handlers.sio)

application = get_wsgi_application()
