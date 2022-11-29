from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.UserList.as_view(), name="register"),
    path('login/', views.login, name="login"),
    path('secret/', views.secret, name="secret"),
    path('public/', views.public, name='public')
]
