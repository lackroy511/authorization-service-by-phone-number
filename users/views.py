from datetime import datetime

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UpdateUserSerializer, UserSerializer
from users.utils import (generate_invitation_code, generate_otp,
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
            personal_invitation_code = user.personal_invitation_code
            
        except User.DoesNotExist:

            personal_invitation_code = generate_invitation_code()
            user = User.objects.create(
                phone=phone,
                personal_invitation_code=personal_invitation_code,
            )

        otp = generate_otp()
        user.otp = otp
        user.save()

        # Тут должна быть отправка смс с кодом на телефон пользователя
        # вместо отправки кода на почту.
        send_otp_email(user.email, otp, personal_invitation_code)

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


class ProfileUpdateAPIView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCurrentUser]
    
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    lookup_field = 'phone'

    def put(self, request, *args, **kwargs):
        
        user = self.request.user
        new_code = self.request.data.get('someone_invite_code')
        old_code = user.someone_invite_code
        
        if new_code != old_code and new_code is not None:
            raise ValidationError('Cannot change someone invite code')
        
        return super().put(request, *args, **kwargs)