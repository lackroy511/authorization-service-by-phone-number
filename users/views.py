from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UserSerializer
from users.utils import (
    generate_invitation_code, generate_otp,
    send_otp_email, validate_phone_number)


class LoginAPIView(APIView):
    
    def post(self, request):

        phone = request.data.get('phone').replace(' ', '').replace('+', '')

        if not phone:
            return Response(
                {'message': 'Необходимо указать телефон "phone"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not validate_phone_number(phone):
            return Response(
                {
                    'message': 'Неверный формат телефона, ' +
                               'должен быть в формате 7 800 800 80 80',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        try:
            
            user = User.objects.get(phone=phone)
            invitation_code = user.invitation_code
        except User.DoesNotExist:

            invitation_code = generate_invitation_code()
            user = User.objects.create(
                phone=phone,
                invitation_code=invitation_code,
            )

        otp = generate_otp()
        user.otp = otp
        user.save()

        # Тут должна быть отправка смс с кодом на телефон пользователя
        # вместо отправки кода на почту.
        send_otp_email(user.email, otp, invitation_code)

        return Response(
            {'message': 'Код отправлен на телефон(почту)'},
            status=status.HTTP_200_OK,
        )


class VerifyAPIView(APIView):

    def post(self, request):

        phone = request.data.get('phone').replace(' ', '').replace('+', '')
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


class ProfileRetrieveAPIView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCurrentUser]
    
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'phone'
