from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserProfileForm, UserRegisterForm
from users.models import CustomUser


# Create your views here.
class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:email_confirmation")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Отключаем возможность логина
        user.generate_token()  # Генерируем токен подтверждения
        user.save()  # Теперь сохраняем в БД

        group = Group.objects.get(name="Пользователи")
        user.groups.add(group)
        verification_url = (
            f"http://{self.request.get_host()}/users/email-confirm/{user.token}/"
        )
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте, перейдите по ссылке для подтверждения почты: {verification_url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


class EmailConfirmationView(TemplateView):
    model = CustomUser
    template_name = "users/email_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено"
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, **kwargs):
        return self.request.user


class UsersListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "users/users_list.html"

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, имеет ли пользователь право на просмотр списка клиентов
        if not request.user.has_perm("users.view_customuser"):
            return HttpResponseForbidden(
                "У вас нет прав для просмотра списка пользователей."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Получаем группу "Пользователи"
        users_group = Group.objects.get(name="Пользователи")

        # Получаем всех пользователей из этой группы, кроме текущего пользователя
        queryset = CustomUser.objects.filter(groups=users_group).exclude(
            id=self.request.user.id
        )
        return queryset


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "users/password_reset_confirm.html"  # Указываем свой шаблон


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
