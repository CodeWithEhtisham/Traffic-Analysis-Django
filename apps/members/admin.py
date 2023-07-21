from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import UserRegistration, UserRegistrationChangeForm
from django.utils.html import format_html

admin.site.site_header = 'Traffic Dashboard'
admin.site.site_title = 'Traffic Dashboard'
admin.site.index_title = 'Traffic Dashboard'

class CustomeUserAdmin(UserAdmin):
    add_form = UserRegistration
    form = UserRegistrationChangeForm
    model = CustomUser

    list_display = ('name','email','phone','company','role','is_staff','is_active','last_login', 'date_joined')
    list_filter = ('cnic','email','company','is_staff','is_active',)
    
    def user_image_tag(self, obj):
        return format_html('<img src="{}" width="240" height="180" />'.format(obj.user_img.url))
    
    user_image_tag.short_description = 'User Image'
    
    readonly_fields = ('user_image_tag',)

    fieldsets = (
    (None, {
        'fields': ('name', 'lastname', 'password')
    }),
    ('Personal Information', {
        'fields': ('age', 'gender', 'city', 'address', 'cnic', 'phone')
    }),
    ('Employment Information', {
        'fields': ('company', 'email', 'role')
    }),
    
    ('Profile Picture', {
        'fields': ('user_img','user_image_tag'),
    }),
    ('Permissions', {
        'fields': ('is_staff', 'is_active', 'groups', 'user_permissions',),
    })
)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name', 'lastname', 'age', 'gender', 'city', 'address', 'cnic',
                'phone', 'company', 'role', 'email','password1', 'password2', 'user_img',
                'is_staff', 'is_active', 'groups', 'user_permissions',
            ),
        }),
    )
    search_fields = ('name', 'cnic', 'company')
    ordering = ('-date_time',)

admin.site.register(CustomUser, CustomeUserAdmin)
