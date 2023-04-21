from django.contrib.auth import password_validation, update_session_auth_hash
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
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'placeholder': 'MM-DD-YYYY'}
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    confirm_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
        required=False,
    )
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
        required=False,
    )
    avatar = forms.ImageField(
        label='Profile photo',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'sex',
            'phone_number',
            'old_password',
            "password",
            "confirm_password",
            'avatar',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        old_password = cleaned_data.get("old_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )
        if old_password and not self.instance.check_password(old_password):
            raise forms.ValidationError(
                "Old password is incorrect"
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        avatar = self.cleaned_data.get('avatar')  # Получаем загруженный файл
        if password is not None and password != '':
            user.set_password(password)
            update_fields = [
                "first_name",
                "last_name",
                "email",
                "birth_date",
                "sex",
                "phone_number",
                "avatar",
                "password",
            ]
            update_session_auth_hash(self.request, user)
        else:
            update_fields = [
                "first_name",
                "last_name",
                "email",
                "birth_date",
                "sex",
                "phone_number",
                "avatar",
            ]
        if commit:
            user.save(update_fields=update_fields)
        return user



