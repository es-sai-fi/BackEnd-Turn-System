
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Role

class CustomUserCreationForm(UserCreationForm):
    role_id = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label="Rol")

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'last_name', 'role_id', 'password1', 'password2')
