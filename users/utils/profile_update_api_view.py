from rest_framework.serializers import ValidationError


def check_invite_code_cant_be_changed(self, request) -> None:
    
    user = self.request.user
    new_code = self.request.data.get('someone_invite_code')
    old_code = user.someone_invite_code

    if new_code:
        if new_code != old_code and old_code is not None:
            raise ValidationError(
                {
                    'message': 'Нельзя изменить код' + 
                               ' пригласившего пользователя',
                },
            )
