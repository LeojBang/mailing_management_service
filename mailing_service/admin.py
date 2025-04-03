from django.contrib import admin

from mailing_service.models import Mailing, MailingAttempt, MailingRecipient, Message

admin.site.register(MailingRecipient)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(MailingAttempt)
