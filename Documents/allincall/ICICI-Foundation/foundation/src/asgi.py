"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.urls import path
from reports import consumers
from channels.routing import ProtocolTypeRouter,URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

application = get_asgi_application()

ws_pattern= [
    path('ws/batches-import/',consumers.ImportBatches),
    path('ws/pizza/',consumers.OrderProgress),
]

application= ProtocolTypeRouter(
    {
        'websocket':(URLRouter(ws_pattern))
    }
)