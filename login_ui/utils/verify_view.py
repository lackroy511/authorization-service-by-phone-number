
import requests


def send_post_user_data(self, phone: str, password: str) -> requests.Response:
    """Отправить данные для аутентификации пользователя.
    Args:
        phone (str): Номер телефона пользователя.
        password (str): Пароль, который будет использоваться 
            для аутентификации.
    Returns:
        requests.Response: Ответ от апи с токеном доступа и обновления.
    """
    return requests.post(
        self.url, data={'phone': phone, 'password': password})
