from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'image', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    username.admin_order_field = 'user__username'
    email.admin_order_field = 'user__email'

admin.site.register(CustomUser, CustomUserAdmin)
