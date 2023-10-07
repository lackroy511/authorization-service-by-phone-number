import requests
from django.http import HttpRequest


def get_current_data_about_user(self, access_token: str) -> requests.Response:
    """Получить информацию о профиле пользователя из апи.
    Args:
        access_token (str): Токен доступа

    Returns:
        requests.Response: Ответ от апи с данными профиля.
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    return requests.get(
        f'{self.url}/retrieve/{self.request.user.phone}/', headers=headers)


def add_user_data_to_context(
        context: dict, response: requests.Response) -> dict:
    """Передать текущие данные пользователя в контекст.
    Args:
        context (dict): Текущий контекст.
        response (requests.Response): Данные из апи.

    Returns:
        dict: Контекст с данными профиля.
    """
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


def post_new_user_data(self, request: HttpRequest) -> None:
    """
    Обновить информацию о профиле пользователя.
    Args:
        request (HttpRequest): Пост запрос.
    """
    access_token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    
    data = get_data_from_post_query(request)
    requests.patch(
            f'{self.url}/update/{self.request.user.phone}/', 
            data=data, headers=headers)


def get_data_from_post_query(request: HttpRequest) -> dict:
    """Получить данные из пост запроса от фронтенда.
    Args:
        request (HttpRequest): запрос от фронтенда.
        
    Returns:
        dict: Данные из пост запроса от фронтенда.
    """
    return {
        'email': request.POST.get('email'),
        'first_name': request.POST.get('first_name'),
        'last_name': request.POST.get('last_name'),
        'someone_invite_code': request.POST.get('someone_invite_code'),
        
    }
