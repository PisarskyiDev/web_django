from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from PIL import Image
from io import BytesIO

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    #
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     context = self.get_context_data(form=form, object=self.object)
    #     user = context['user']
    #     avatar = user.avatar  # Получаем объект Avatar для пользователя
    #     context['avatar'] = avatar  # Добавляем объект Avatar в контекст шаблона
    #     return self.render_to_response(context)
    #

    # def post_avatar(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         user = self.get_object()
    #         avatar = form.cleaned_data.get('avatar')  # Получаем загруженный файл
    #         if avatar:
    #             user.avatar.delete()  # Удаляем старый файл аватара пользователя
    #             user.avatar = avatar  # Сохраняем новый файл аватара пользователя
    #         user.avatar.save()
    #         # messages.success(request, 'Your profile has been updated successfully.')
    #         return redirect('app_main:profile', pk=user.pk)
    #     else:
    #         return self.form_invalid(form)
