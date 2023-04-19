from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileForm
from .models import CustomUser


def index(request):
    return render(request, "index.html")


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('app_main:login')
    template_name = 'registration/signup.html'


class LoginView(generic.FormView):
    form_class = CustomAuthenticationForm
    success_url = '/'
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


# class ProfileView(LoginRequiredMixin, generic.DetailView):
#     model = CustomUser
#     template_name = 'profile.html'
#     context_object_name = 'user'
#
#     def test_func(self):
#         return self.request.user.is_authenticated and self.get_object() == self.request.user
#
#     def handle_no_permission(self):
#         return redirect('app_main:home')

# @method_decorator(login_required, name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'profile.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def test_func(self):
        return self.request.user.is_authenticated and self.get_object() == self.request.user

    def handle_no_permission(self):
        return redirect('app_main:home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('app_main:profile', kwargs={'pk': self.request.user.pk})



