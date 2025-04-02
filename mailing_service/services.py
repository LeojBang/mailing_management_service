from django.core.mail import send_mail
from django.utils import timezone
from config.settings import EMAIL_HOST_USER
from mailing_service.models import Mailing, MailingAttempt


class MailingService:
    @staticmethod
    def start_mailing(mailing: Mailing):
        mailing.start_time = timezone.now()
        mailing.status = "Запущена"
        mailing.save()

        subject = mailing.message.subject
        message = mailing.message.body
        recipients = mailing.recipients.all()

        successful = 0
        failed = 0

        for recipient in recipients:
            try:
                send_mail(
                    subject,
                    message,
                    EMAIL_HOST_USER,
                    [recipient.email]
                )
                status = "Success"
                server_response = "Отправлено успешно"
                successful += 1
            except Exception as e:
                status = "Failed"
                server_response = str(e)
                failed += 1

            # Запись попытки отправки письма
            MailingAttempt.objects.create(
                status=status,
                server_response=server_response,
                mailing=mailing
            )

        # Обновление статистики рассылки
        mailing.successful_attempts += successful
        mailing.failed_attempts += failed
        mailing.total_messages_sent += successful
        mailing.end_time = timezone.now()

        # Устанавливаем корректный статус рассылки
        if successful == len(recipients):
            mailing.status = "Completed"
        elif failed == len(recipients):
            mailing.status = "Failed"
        else:
            mailing.status = "Partially Completed"

        mailing.save()