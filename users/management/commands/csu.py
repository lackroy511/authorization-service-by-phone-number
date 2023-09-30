from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        user = User.objects.create(
            email='1',
            phone='1',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        
        user.set_password('1')
        user.save()
