from django.urls import path 
from . import views 

urlpatterns = [
    path('channel-list-api/', views.ChannelListAPIView.as_view(), name="channel_list_api")
]
