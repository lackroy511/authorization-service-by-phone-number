from typing import Any

import requests
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import status

from login_ui.utils.profile_view import (add_user_data_to_context,
                                         get_current_data_about_user,
                                         post_new_user_data)
from login_ui.utils.verify_view import send_post_user_data
from users.models import User

# Create your views here.


class IndexView(TemplateView):
    """Главная страница с вводом номера телефона."""
    template_name = 'login_ui/index.html'
    url = 'http://127.0.0.1:8000/users/login/'
    
    def post(self, request):
        """
        Получить телефон пользователя из пост запроса от фронтенда.
        Отправить телефон на эндпоинт апи, где на номер телефона(почту)
        отправляется сгенерированный пароль.
        """
        phone = request.POST.get('phone')
        response = requests.post(self.url, data={'phone': phone})
        response = response.json()
        request.session['phone'] = phone
        # request.session['response'] = response
        
        return redirect('login_ui:verify')


class VerifyView(TemplateView):
    """
    Подтверждение номера телефона с помощью случайного пароля,
    отправленного на почту(телефон).
    """
    template_name = 'login_ui/verify.html'
    
    url = 'http://127.0.0.1:8000/users/verify/'
    
    def get_context_data(self, **kwargs):
        """
        Добавить в контекст телефон из сессии что бы он отображался
        в строке ввода телефона по дефолту.
        """
        
        context = super().get_context_data(**kwargs)
        phone = self.request.session.get('phone')
        context['phone'] = phone
        
        return context
        
    def post(self, request):
        """
         Получить телефон и пароль пользователя из пост запроса с фронтенда.
         После получения телефона и пароля отправить их для аутентификации
        на апи, что бы получить токен доступа и токен обновления.
         Отправить токен доступа и токен обновления в сессию, 
        для дальнейшего использования.
         Затем залогинить пользователя, если данные верны.
        """
        phone = request.POST.get('phone').replace(' ', '').replace('+', '')
        password = request.POST.get('password')
        
        response = send_post_user_data(self, phone, password)
        
        if response.status_code == status.HTTP_200_OK:
            response = response.json()
            
            access_token = response.get('access_token')
            refresh_token = response.get('refresh_token')
            
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            
            user = User.objects.get(phone=phone)
            login(request, user)
        
        return redirect('login_ui:index')


class ProfileView(TemplateView):
    """Просмотр и обновление профиля пользователя."""
    
    template_name = 'login_ui/profile.html'
    
    url = 'http://127.0.0.1:8000/users'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Отправить текущую информацию о профиле пользователя в шаблон."""
        context = super().get_context_data(**kwargs)
        
        access_token = self.request.session.get('access_token')
        response = get_current_data_about_user(self, access_token)
        
        if response.status_code == status.HTTP_200_OK:
            add_user_data_to_context(context, response)           
        
        return context
    
    def post(self, request):
        """Обновить информацию о профиле пользователя."""
        post_new_user_data(self, request)
        
        return redirect('login_ui:profile')
