

from users.models import User
from users.utils.utils import generate_invitation_code


def user_get_or_create(phone_number: str) -> User:
    
    try:
        user = User.objects.get(phone=phone_number)

    except User.DoesNotExist:
        user = User.objects.create(
            phone=phone_number,
            personal_invitation_code=generate_invitation_code())
    
    return user
