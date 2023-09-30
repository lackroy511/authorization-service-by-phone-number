from django.urls import path

from users.apps import UsersConfig
from users.views import LoginAPIView, ProfileRetrieveAPIView, VerifyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('profile/<str:phone>/', 
         ProfileRetrieveAPIView.as_view(), name='profile'),
]
