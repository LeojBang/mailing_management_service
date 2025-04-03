from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailing_service.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = 'Отправка всех рассылок со статусом "Created"'

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(
            status="Created"
        )  # Отправляем только не запущенные рассылки
        for mailing in mailings:
            recipients = mailing.recipients.all()
            subject = mailing.message.subject
            body = mailing.message.body

            success_count = 0
            errors = []

            for recipient in recipients:
                try:
                    sent_count = send_mail(
                        subject, body, EMAIL_HOST_USER, [recipient.email]
                    )
                    success_count += sent_count
                except Exception as e:
                    errors.append(f"Ошибка для {recipient.email}: {str(e)}")

            # Фиксируем попытку рассылки
            mailing_attempt = MailingAttempt.objects.create(
                status="Success" if success_count == len(recipients) else "Failed",
                server_response="\n".join(errors)
                or f"Отправлено {success_count} из {len(recipients)}",
                mailing=mailing,
            )

            # Обновляем статус рассылки
            mailing.status = (
                "Completed" if success_count == len(recipients) else "Running"
            )
            mailing.end_time = timezone.now()
            mailing.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Рассылка {mailing.id} завершена: {mailing_attempt.status}"
                )
            )
