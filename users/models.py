from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    username = None
    
    phone = models.CharField(
        max_length=11, 
        unique=True,
        verbose_name='номер телефона',
    )
    otp = models.CharField(
        max_length=4, 
        blank=True, null=True,
        verbose_name='одноразовый пароль',
    )
    personal_invitation_code = models.CharField(
        max_length=6,
        verbose_name='мой код приглашения',
        unique=True,
        null=True, blank=True,
    )
    someone_invite_code = models.CharField(
        default=None,
        max_length=6,
        verbose_name='чей-то код приглашения',
        null=True, blank=True,
    )
    
    def __str__(self):
        return self.phone
