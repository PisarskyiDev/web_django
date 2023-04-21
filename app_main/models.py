import uuid

from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    SEX_CHOICES = [
        ("Male", 'Male'),
        ("Female", 'Female'),
        ("Other", 'Other'),
    ]
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=128, validators=[validate_password], help_text='Max symbols is 16')
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/profile', null=True, blank=True,)

    def get_absolute_url(self):
        return reverse('app_main:profile', args=[str(self.key)])

