from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UpdateUserSerializer, UserSerializer
from users.tasks import send_otp_to_email
from users.utils.doc import (login_api_doc, profile_update_api_doc,
                             refresh_api_doc, verify_api_doc)
from users.utils.login_api_view import user_get_or_create
from users.utils.profile_update_api_view import \
    check_invite_code_cant_be_changed
from users.utils.utils import (error_message_response_400,
                               error_message_response_401,
                               error_message_response_404,
                               error_message_response_422, generate_otp,
                               success_response, success_response_with_token,
                               validate_phone_number)


class LoginAPIView(APIView):
    """
     Эндпоинт принимает пост запрос с номером телефона и создает пользователя 
    или генерирует новый пароль для входа, если пользователь уже существует.
     Затем отправляет на почту код для аутентификации.
    """
    
    @login_api_doc()
    def post(self, request):

        phone = request.data.get('phone')
        if phone:
            phone = phone.replace(' ', '').replace('+', '')
            
        if not phone:
            message = 'Необходимо указать телефон "phone"'
            return error_message_response_400(message)

        if not validate_phone_number(phone):
            message = 'Неверный формат телефона, ' + \
                      'должен быть в формате 7 800 800 80 80'
            return error_message_response_400(message)

        user = user_get_or_create(phone)
        otp = generate_otp()
        user.set_password(otp)
        user.save()

        # Тут должна быть отправка смс с кодом на телефон пользователя
        # вместо отправки кода на почту.
        send_otp_to_email.delay(user.email, otp, user.personal_invitation_code)

        message = 'Код отправлен на телефон(почту)'
        return success_response(message)


class VerifyAPIView(APIView):
    """
     Эндпоинт принимает код отправленный на почту и обновляет пароль 
    пользователя на неизвестный для него.
     Если пароль верный выдает токен обновления и токен доступа.
    """
    
    @verify_api_doc()
    def post(self, request):

        phone = request.data.get('phone')
        if phone:
            phone = phone.replace(' ', '').replace('+', '')
            
        password = request.data.get('password')

        if not phone or not password:
            message = 'Укажите: "phone" и "password"'
            return error_message_response_400(message)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            message = 'Такого пользователя не существует'
            return error_message_response_404(message)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            # Обновить пароль пользователя, 
            # что бы ограничить аутентификацию только через полученный токен.
            user.set_password(generate_otp())
            user.save()

            return success_response_with_token(refresh)
        
        message = 'Неверный пароль'
        return error_message_response_401(message)


class RefreshTokenAPIView(APIView):
    
    @refresh_api_doc()
    def post(self, request):

        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            message = 'Укажите: "refresh_token'
            return error_message_response_400(message)

        try:
            refresh = RefreshToken(refresh_token)
            
        except TokenError:
            message = 'Неверный токен'
            return error_message_response_422(message)

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

    @profile_update_api_doc()
    def put(self, request, *args, **kwargs):

        check_invite_code_cant_be_changed(self, request)

        return super().put(request, *args, **kwargs)
    
    @profile_update_api_doc()
    def patch(self, request, *args, **kwargs):
        
        check_invite_code_cant_be_changed(self, request)
        
        return super().patch(request, *args, **kwargs)
