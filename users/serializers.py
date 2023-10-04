from rest_framework import serializers

from users.models import User
from users.validators import InviteCodeIsExist


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:    
        model = User
        fields = (
            'id', 
            'email',
            'phone',
            'first_name', 
            'last_name',
            'personal_invitation_code',
            'someone_invite_code',
            'invited_users',
        )

    invited_users = serializers.SerializerMethodField()
    
    def get_invited_users(self, obj):
        
        return User.objects.filter(
            someone_invite_code=obj.personal_invitation_code,
        ).values('phone')
        

class UpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta:    
        model = User
        fields = ( 
            'email',
            'first_name', 
            'last_name',
            'someone_invite_code',
        )        
        validators = (
            InviteCodeIsExist(),
        )
