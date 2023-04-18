from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'sex',
            'birth_date',
        )


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser

