"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# application = get_asgi_application()

import os
import django
import socketio

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

django.setup()

sio = socketio.Server(async_mode='asgi')
app = socketio.ASGIApp(sio)

from apps.analysis import socket_handlers

sio.register_namespace(socket_handlers.sio)

application = get_asgi_application()
