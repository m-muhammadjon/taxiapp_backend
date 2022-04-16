from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('ws/user/<int:user_id>/', consumers.UserConsumer.as_asgi()),

]
