from django.urls import re_path

from .consumers import BookConsumer

websocket_urlpatterns = [
    re_path(r'^ws/ioplibrary/$', BookConsumer.as_asgi()),
]