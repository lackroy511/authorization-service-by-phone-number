import random
import re
import string

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def generate_otp(length: int = 4) -> str:
    
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))
    

def validate_phone_number(phone_number: str) -> bool:
    
    result = re.fullmatch(r'[7][0-9]{10}', phone_number.replace(' ', ''))
    return True if result is not None else False


def generate_invitation_code(length: int = 6) -> str:
    
    symbols = string.ascii_lowercase + string.digits
    return ''.join(random.choice(symbols) for i in range(length))


def success_response(message: str) -> Response:
    return Response(
            {'message': f'{message}'},
            status=status.HTTP_200_OK,
        )


def success_response_with_token(refresh: RefreshToken) -> Response:
    return Response(
        {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        },
        status=status.HTTP_200_OK)


def error_message_response_400(message: str) -> Response:
    
    return Response(
        {'message': f'{message}'}, status=status.HTTP_400_BAD_REQUEST)


def error_message_response_404(message: str) -> Response:
    
    return Response(
        {'message': f'{message}'}, status=status.HTTP_404_NOT_FOUND)


def error_message_response_401(message: str) -> Response:
    
    return Response(
        {'message': f'{message}'}, status=status.HTTP_401_UNAUTHORIZED)


def error_message_response_422(message: str) -> Response:
    
    return Response(
        {'message': f'{message}'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
