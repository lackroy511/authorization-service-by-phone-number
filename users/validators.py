from collections import OrderedDict
from rest_framework.serializers import ValidationError

from users.models import User


class CantChangeSomeoneInviteCode:
    
    def __call__(self, fields: OrderedDict) -> None:
        
        phone = fields.get('phone')
        user = User.objects.get(phone=phone)
        
        new_code = fields.get('someone_invite_code')
        old_code = user.someone_invite_code
        
        print(new_code, old_code)
        
        if new_code != old_code and new_code is not None:
            raise ValidationError('Cannot change someone invite code')
