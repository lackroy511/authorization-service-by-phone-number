import random
import re
import string

from django.conf import settings
from django.core.mail import send_mail

from users.models import User


def generate_otp(length: int = 4) -> str:
    
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))
    

def validate_phone_number(phone_number: str) -> bool:
    
    result = re.fullmatch(r'[7][0-9]{10}', phone_number.replace(' ', ''))
    return True if result is not None else False


def generate_invitation_code(length: int = 6) -> str:
    
    symbols = string.ascii_lowercase + string.digits
    return ''.join(random.choice(symbols) for i in range(length))
