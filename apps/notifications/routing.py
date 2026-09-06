from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/live-tracking/(?P<request_id>\d+)/$', consumers.LiveTrackingConsumer.as_asgi()),
    re_path(r'ws/control-room/$', consumers.ControlRoomConsumer.as_asgi()),
]
