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
            200: openapi.Response(
                'Success', openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Код отправлен на телефон(почту)',
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                'Bad request', openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            example='Неверный формат телефона, должен быть' + 
                                    'в формате 7 800 800 80 80',
                        ),
                    },
                ),
            ),
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
            200: openapi.Response(
                description='Success',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Токен доступа',
                            example='eyJhbGJfj3jb...gqFDHLsvK0',
                        ),
                        'refresh_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Токен обновления',
                            example='eyJhbGJfj3jb...gqFDHLsvK0',
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                'Bad request', openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            example='Укажите: "phone" и "password"',
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                'Unauthorized', openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            example='Неверный пароль',
                        ),
                    },
                ),
            ),
            404: openapi.Response(
                'Not found', openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            example='Такого пользователя не существует',
                        ),
                    },
                ),
            ),
            403: openapi.Response(
                'Forbidden', openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            example='You do not have permission to perform' + 
                                    'this action.',
                        ),
                    },
                ),
            ),
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
                description='Success',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Ответ сервера',
                            example='eyJhbGJfj3jb...gqFDHLsvK0',
                        ),
                    },
                ),
            ),
            422: openapi.Response(
                'Invalid token', openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            example='Неверный токен',
                        ),
                    },
                ),
            ),
        },
    )


def profile_update_api_doc():
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Электронная почта',
                    example='qwe@qwe.com',
                ),
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Имя',
                    example='Юра',
                ),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Фамилия',
                    example='Дудь',
                ),
                'someone_invite_code': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Инвайт код пользователя, который пригласил',
                    example='enxt0g',
                ),
            },
        ),
        responses={
            400: openapi.Response(
                'Bad request', openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            example='Нельзя изменить код пригласившего' + 
                                    'пользователя',
                        ),
                    },
                ),
            ),
            404: openapi.Response(
                'Not found', openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            example='Not found.',
                        ),
                    },
                ),
            ),
            403: openapi.Response(
                'Forbidden', openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            example='You do not have permission to perform' + 
                                    'this action.',
                        ),
                    },
                ),
            ),
        },
    )
