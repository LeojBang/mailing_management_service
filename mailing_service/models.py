from django.db import models
from django.utils import timezone

from users.models import CustomUser


class MailingRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='Ф. И. О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Текст письма')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    start_time = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время последней отправки')
    STATUS_CHOICES = [
        ('Completed', 'Завершена'),
        ('Created', 'Создана'),
        ('Running', 'Запущена'),
    ]
    status = models.CharField(choices=STATUS_CHOICES, default='Created', verbose_name='Статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    recipients = models.ManyToManyField(MailingRecipient, verbose_name='Получатели')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    successful_attempts = models.PositiveIntegerField(default=0)
    failed_attempts = models.PositiveIntegerField(default=0)
    total_messages_sent = models.PositiveIntegerField(default=0)

    def check_status(self):
        """Проверка статуса рассылки на основе текущего времени."""
        if timezone.now() > self.end_time:
            self.status = 'Completed'
            self.save()


    def __str__(self):
        return f"Рассылка {self.id} ({self.status})"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ("can_disable_mailing", "Can disable mailing"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('Success', 'Успешно'),
        ('Failed', 'Не успешно'),
    ]
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='Статус рассылки')
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    server_response = models.TextField(blank=True, verbose_name='Ответ сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f"Попытка {self.id} ({self.status})"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'