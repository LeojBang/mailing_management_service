from django.contrib import admin

from mailing_service.models import MailingRecipient, Message, Mailing

admin.site.register(MailingRecipient)
admin.site.register(Message)
admin.site.register(Mailing)
