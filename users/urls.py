from django.urls import path

from users.apps import UsersConfig
from users.views import LoginAPIView, VerifyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
]
