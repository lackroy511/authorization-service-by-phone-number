from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import os


@shared_task()
def send_otp_to_email(email: str, otp: str, invitation_code: str) -> None:
    
    subject = 'Password for your account'
    message = f'Ваш код для входа: {otp} \nВаш инвайт код: {invitation_code}'
    from_email = settings.EMAIL_HOST_USER
    
    # Адрес для тестовых сообщений
    recipient_list = [os.getenv('RECIPIENT_EMAIL')]  
    send_mail(subject, message, from_email, recipient_list)


@shared_task()
def send_otp_to_phone_number():
    pass
