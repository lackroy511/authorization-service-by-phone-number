from typing import Any
from django import http
import requests
from rest_framework import status
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from users.models import User

# Create your views here.


class IndexView(TemplateView):
    template_name = 'login_ui/index.html'
    
    url = 'http://127.0.0.1:8000/users/login/'
    
    def post(self, request, *args, **kwargs):
        
        phone = request.POST.get('phone')
        response = requests.post(self.url, data={'phone': phone})
        response = response.json()
        request.session['phone'] = phone
        request.session['response'] = response
        
        return redirect('login_ui:verify')


class VerifyView(TemplateView):
    template_name = 'login_ui/verify.html'
    
    url = 'http://127.0.0.1:8000/users/verify/'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        phone = self.request.session.get('phone')
        
        context = super().get_context_data(**kwargs)
        context['phone'] = phone
        return context
        
    def post(self, request, *args, **kwargs):
        
        phone = request.POST.get('phone').replace(' ', '').replace('+', '')
        password = request.POST.get('password')
        
        response = requests.post(
            self.url, data={'phone': phone, 'password': password})
        
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
    template_name = 'login_ui/profile.html'
    
    url = 'http://127.0.0.1:8000/users'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        context = super().get_context_data(**kwargs)
        
        access_token = self.request.session.get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'}
        
        response = requests.get(
            f'{self.url}/retrieve/{self.request.user.phone}/', headers=headers)
        
        if response.status_code == status.HTTP_200_OK:
            response = response.json()
            
            context['phone'] = response.get('phone')  
            context['email'] = response.get('email')   
            context['first_name'] = response.get('first_name')    
            context['last_name'] = response.get('last_name')    
            context['personal_invitation_code'] = \
                response.get('personal_invitation_code')    
            context['someone_invite_code'] = \
                response.get('someone_invite_code')    
            context['invited_users'] = response.get('invited_users')           
        
        return context
    
    def post(self, request, *args, **kwargs):
        
        access_token = request.session.get('access_token')
        
        headers = {'Authorization': f'Bearer {access_token}'}
        
        data = {
            'email': request.POST.get('email'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'someone_invite_code': request.POST.get('someone_invite_code'),
        }
        
        requests.patch(
            f'{self.url}/update/{self.request.user.phone}/', 
            data=data, headers=headers)
        
        return redirect('login_ui:profile')
