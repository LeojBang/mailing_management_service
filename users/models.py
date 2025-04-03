import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="media/avatars",
        help_text="Загрузите свой аватар",
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Страна",
        help_text="Введите страну проживания",
    )
    token = models.CharField(unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # Флаг подтверждения email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_block_user", "Сan block user"),
        ]

    def __str__(self):
        return self.email

    def generate_token(self):
        """Генерирует уникальный токен"""
        self.token = secrets.token_hex(16)
        self.save()
