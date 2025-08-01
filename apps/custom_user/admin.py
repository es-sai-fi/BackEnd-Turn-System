
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Role
from .forms import CustomUserCreationForm

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('email', 'name', 'last_name', 'role_id', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')  # ← QUITA 'groups'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('name', 'last_name', 'age', 'priority', 'role_id')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'last_name', 'age', 'priority', 'role_id', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
