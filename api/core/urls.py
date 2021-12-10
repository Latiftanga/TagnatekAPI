from django.urls import path
from core import views


app_name = 'core'


urlpatterns = [
    path('login', views.login, name='login'),
    path('user', views.AuthenticatedUser.as_view(), name='current_user'),
    path('create', views.CreateUserAPIView.as_view(), name='create_user'),
    path('token', views.CreateTokenAPIView.as_view(), name='token'),
    path('me', views.ManageUserView.as_view(), name='me'),
    ]
