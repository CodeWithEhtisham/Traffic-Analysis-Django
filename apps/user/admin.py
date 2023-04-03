from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import UserRegisterationForm, UserRegisterationChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterationForm
    form = UserRegisterationChangeForm
    model = CustomUser
    list_display = ('user_name', 'cnic', 'email', 'is_active', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('cnic', 'date_joined', )
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                'user_name', 'last_name', 'address', 'cnic', 'phone',
                'email', 'user_img', "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ('-date_joined',)

admin.site.register(CustomUser, CustomUserAdmin)
