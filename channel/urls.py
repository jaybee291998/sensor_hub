from django.urls import path 
from . import views 

urlpatterns = [
    path('channel-list-api/', views.ChannelListAPIView.as_view(), name="channel_list_api"),
    path('field-list/<int:channel_id>/', views.FieldListAPIView.as_view(), name="field_list"),
    path('<int:channel_id>/', views.ChannelEntryListAPIView.as_view(), name="channel"),
    path('update/', views.ChannelEntryAPIView.as_view(), name="update_channel"),
    path('wakemeup/', views.WakeMeUpAPIView.as_view(), name="wake_me_up")
]
