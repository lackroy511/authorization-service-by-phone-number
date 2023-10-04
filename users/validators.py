from collections import OrderedDict
from typing import Any

from rest_framework.request import Request
from rest_framework.serializers import ValidationError

from users.models import User


class InviteCodeIsExist:

    def __call__(self, fields: OrderedDict) -> Any:

        invite_code = fields.get('someone_invite_code')
        
        if invite_code:
            flag = User.objects.filter(
                personal_invitation_code=invite_code).exists()
        
            if not flag:
                raise ValidationError(
                    {'message': 'Код приглашения не существует'})


class CantChangeInviteCode:
    
    def __call__(self, fields: OrderedDict, request: Request) -> Any:
        
        print(request)
