"""
URL configuration for web_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LogoutView
from django.urls import path

from app_main.views import (
    index,
    SignUpView,
    LoginView,
    # ProfileView
    # profile_view,
    ProfileUpdateView,
)

urlpatterns = [
    path('', index, name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("profile/<int:pk>/", ProfileView.as_view(),  name="profile")
    # path("profile/<int:pk>/", profile_view,  name="profile")
    path("profile/<int:pk>/", ProfileUpdateView.as_view(),  name="profile")
]

app_name = "app_main"
