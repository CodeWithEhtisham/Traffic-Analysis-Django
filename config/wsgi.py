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
import threading

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from apps.analysis.views import run_socketio_server #,receive_frames,callback_detection


threading.Thread(target=run_socketio_server).start()
# threading.Thread(target=receive_frames).start()
# threading.Thread(target=callback_detection).start()

# thread.start()
print('SocketIO server running on port 7000')
# sio = socketio.Server(async_mode='threading')

# from apps.analysis.socket_handlers import sio
# app = socketio.WSGIApp(sio)

# sio.WSGIApp(socket_handlers.sio)
# thread = threading.Thread(target=run_socketio_server)
# thread.start()

application = get_wsgi_application()
