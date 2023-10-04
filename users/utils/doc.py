from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def login_api_doc():
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Номер телефона пользователя' +
                                '(формат: 7 800 800 80 80)',
                    example='7 800 800 80 80',
                ),
            },
            required=['phone'],
        ),
        responses={
            200: 'Код отправлен на телефон(почту)',
            400: 'Некорректные данные запроса',
        },
    )


def verify_api_doc():
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Номер телефона пользователя ' +
                                '(формат: 7 800 800 80 80)',
                    example='7 800 800 80 80',
                ),
                'otp': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Код аутентификации (формат: 3412)',
                    example='1221',
                ),
            },
            required=['phone', 'otp'],
        ),
        responses={
            200: 'access_token и refresh_token',
            400: 'Укажите: "phone" и "password"',
            404: 'Такого пользователя не существует',
            401: 'Код не совпадает',
        },
    )


def refresh_api_doc():
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Токен обновления',
                    example='eyJhbGJfj3jb...gqFDHLsvK0',
                ),
            },
            required=['phone'],
        ),
        responses={
            200: openapi.Response(
                description='Токен доступа',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Токен доступа',
                            example='eyJhbGJfj3jb...gqFDHLsvK0',
                        ),
                    },
                ),
            ),
            400: 'Укажите: "refresh_token',
        },
    )


def profile_update_api_doc():
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'someone_invite_code': 
                    openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={400: 'Нельзя изменить код пригласившего пользователя'},
    )
