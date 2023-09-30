import string
import random

from django.core.mail import send_mail
from django.conf import settings


def generate_otp(length: int = 4) -> str:
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))
    

def generate_invitation_code(length: int = 6) -> str:
    symbols = string.ascii_lowercase + string.digits
    return ''.join(random.choice(symbols) for i in range(length))
    
    
def send_otp_email(email: str, otp: str) -> None:
    
    subject = 'Password for your account'
    message = f'Your password is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['lackroy511@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
