from rest_framework.serializers import ValidationError


def check_invite_code_cant_be_changed(self) -> None:
    """Если код уже существует и его пытаются изменить, вызвать ошибку.
    Raises:
        ValidationError: Ошибка при попытке изменения уже существующего 
                         кода приглашения
    """
    new_code = self.request.data.get('someone_invite_code')
    old_code = self.request.user.someone_invite_code
    message = 'Нельзя изменить код пригласившего пользователя'
    
    if new_code:
        if new_code != old_code and old_code is not None and old_code != '':
            raise ValidationError(
                {
                    'message': message,
                },
            )

    if new_code == '' and (old_code != '' and old_code is not None):
        raise ValidationError(
                {
                    'message': message,
                },
            )
