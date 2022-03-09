import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import django
django.setup()

#from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import mos.backend.routing

application = ProtocolTypeRouter({
    #"http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mos.backend.routing.websocket_urlpatterns
        )
    ),
})
