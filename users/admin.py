from django.contrib import admin

from users.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'email', 
        'phone',
        'personal_invitation_code',
        'someone_invite_code',
        'otp', 
        'password', 
        'is_active', 
        'is_staff', 
        'is_superuser',
    )
