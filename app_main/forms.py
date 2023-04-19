from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import DateInput

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

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


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'MM-DD-YYYY'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'sex', 'phone_number']


