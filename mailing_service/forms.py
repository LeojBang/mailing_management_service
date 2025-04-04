from django import forms
from django.forms import ModelForm

from mailing_service.models import Mailing, MailingRecipient, Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
        widgets = {
            "subject": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите тему письма"}
            ),
            "body": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Введите текст письма"}
            ),
        }


class MailingRecipientForm(ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ["email", "full_name", "comment"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите email получателя",
                }
            ),
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите Ф. И. О. получателя",
                }
            ),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Введите комментарий"}
            ),
        }


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "recipients"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите дату и время первой отправки",
                    "input_format": "%Y-%m-%d %H:%M:%S",
                }
            ),
            "end_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите дату и время последней отправки",
                    "input_format": "%Y-%m-%d %H:%M:%S",
                }
            ),
            "message": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Выберите сообщение для рассылки",
                }
            ),
            "recipients": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                    "placeholder": "Выберите получателей рассылки",
                }
            ),
        }
