from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UpdateUserSerializer, UserSerializer
from users.tasks import send_otp_to_email
from users.utils.login_api_view import user_get_or_create
from users.utils.utils import (generate_otp,
                               validate_phone_number)


class LoginAPIView(APIView):
    """
     Эндпоинт принимает пост запрос с номером телефона и создает пользователя 
    или генерирует новый пароль для входа, если пользователь уже существует.
     Затем отправляет на почту код для аутентификации.
    """
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

        user = user_get_or_create(phone)

        otp = generate_otp()
        user.set_password(otp)
        user.save()

        # Тут должна быть отправка смс с кодом на телефон пользователя
        # вместо отправки кода на почту.
        send_otp_to_email.delay(user.email, otp, user.personal_invitation_code)

        return Response(
            {'message': 'Код отправлен на телефон(почту)'},
            status=status.HTTP_200_OK,
        )


class VerifyAPIView(APIView):
    """
     Эндпоинт принимает код отправленный на почту и обновляет пароль 
    пользователя на неизвестный для него.
     Если пароль верный выдает токен обновления и токен доступа.
    """
    def post(self, request):

        phone = request.data.get('phone').replace(' ', '').replace('+', '')
        password = request.data.get('password')

        if not phone or not password:
            return Response(
                {'message': 'Укажите: "phone" и "password"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response(
                {'message': 'Такого пользователя не существует'},
                status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            # Обновить пароль пользователя, 
            # что бы ограничить аутентификацию только через полученный токен.
            user.set_password(generate_otp())
            user.save()

            return Response(
                {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                },
                status=status.HTTP_200_OK)

        return Response(
            {'message': 'Код не совпадает'},
            status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenAPIView(APIView):
    def post(self, request):

        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response(
                {'message': 'Укажите: "refresh_token"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            
        except TokenError:
            return Response({'message': 'Не валидный токен'})

        return Response({'access_token': str(refresh.access_token)})


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsCurrentUser]

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'phone'


class ProfileUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsCurrentUser]

    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    lookup_field = 'phone'

    def put(self, request, *args, **kwargs):

        user = self.request.user
        new_code = self.request.data.get('someone_invite_code')
        old_code = user.someone_invite_code

        if new_code:
            if new_code != old_code and old_code is not None:
                raise ValidationError(
                    {
                        'message': 'Нельзя изменить код' + 
                                   'пригласившего пользователя',
                    })

        return super().put(request, *args, **kwargs)
