from django.urls import path

from users.apps import UsersConfig
from users.views import (LoginAPIView, ProfileRetrieveAPIView,
                         ProfileUpdateAPIView, RefreshTokenAPIView,
                         VerifyAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('refresh/', RefreshTokenAPIView.as_view(), name='refresh'),
    path('retrieve/<str:phone>/', 
         ProfileRetrieveAPIView.as_view(), name='retrieve'),
    path('update/<str:phone>/', ProfileUpdateAPIView.as_view(), name='update'),
]
