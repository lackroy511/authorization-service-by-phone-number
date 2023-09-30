from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.utils import generate_otp, send_otp_email
from users.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class LoginAPIView(APIView):

    def post(self, request):

        phone = request.data.get('phone')
        
        if not phone:
            return Response(
                {'message': 'Необходимо указать телефон "phone"'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            user = User.objects.create(
                phone=phone,
            )

        otp = generate_otp()
        user.otp = otp
        user.save()

        # Тут должна быть отправка смс с кодом на телефон пользователя.
        send_otp_email(user, otp)
        print(otp)

        return Response(
            {'message': 'Код отправлен на телефон(почту)'},
            status=status.HTTP_200_OK,
        )


class VerifyAPIView(APIView):
    
    def post(self, request):
        
        phone = request.data.get('phone')
        otp = request.data.get('otp')
        
        if not phone or not otp:
            return Response(
                {'message': 'Необходимо указать телефон "phone" и код "otp"'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response(
                {'message': 'Такого пользователя не существует'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.otp == otp:
            user.otp = None
            user.save()
            
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {'token': token.key},
                status=status.HTTP_200_OK,
            )
        
        return Response(
            {'message': 'Код не совпадает'},
            status=status.HTTP_400_BAD_REQUEST,
        )
