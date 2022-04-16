import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

import taxi.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxiapp_backend.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            taxi.routing.ws_urlpatterns
        )
    )
})
