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
    email_or_username = forms.CharField(
        max_length=255,
        label='Email or Username'
    )

    class Meta:
        model = CustomUser
        forms = ['username', 'password']

    def clean(self):
        email_or_username = self.cleaned_data.get('email_or_username')
        password = self.cleaned_data.get('password')

        if email_or_username and password:
            user = authenticate(
                request=self.request,
                username=email_or_username,
                password=password,
            )

            if user is None:
                user = authenticate(
                    requset=self.request,
                    email=email_or_username,
                    password=password,
                )

            if user is None:
                raise forms.ValidationError(
                    'The specified email or username does not exist'
                )

            self.user_cache = user
            if not self.user_cache.is_active:
                raise forms.ValidationError(
                    'This account was deactivated'
                )

        return self.cleaned_data
