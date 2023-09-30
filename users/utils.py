import random
import re
import string

from django.conf import settings
from django.core.mail import send_mail


def generate_otp(length: int = 4) -> str:
    
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))
    

def generate_invitation_code(length: int = 6) -> str:
    
    symbols = string.ascii_lowercase + string.digits
    return ''.join(random.choice(symbols) for i in range(length))
    
    
def send_otp_email(email: str, otp: str, invitation_code: str) -> None:
    
    subject = 'Password for your account'
    message = f'Ваш код для входа: {otp} \nВаш инвайт код: {invitation_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['lackroy511@gmail.com']
    send_mail(subject, message, from_email, recipient_list)


def validate_phone_number(phone_number: str) -> bool:
    
    result = re.fullmatch(r'[7][0-9]{10}', phone_number.replace(' ', ''))
    return True if result is not None else False
