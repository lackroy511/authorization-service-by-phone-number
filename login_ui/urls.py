from django.urls import path

from login_ui.apps import LoginUiConfig
from login_ui.views import IndexView, VerifyView, ProfileView
from django.contrib.auth.views import LogoutView

app_name = LoginUiConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
]
