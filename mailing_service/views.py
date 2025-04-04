from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailing_service.forms import (MailingForm, MailingRecipientForm,
                                   MessageForm)
from mailing_service.models import Mailing, MailingRecipient, Message
from mailing_service.services import MailingService, get_data_from_cache


# Create your views here.
class HomeView(TemplateView):
    template_name = "mailing_service/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_count = Mailing.objects.all().count()
        mailing_count_active = Mailing.objects.filter(status="Running").count()
        mailing_recipient_count = MailingRecipient.objects.count()
        context["mailing_count"] = mailing_count
        context["mailing_count_active"] = mailing_count_active
        context["mailing_recipient_count"] = mailing_recipient_count
        return context


class MailingRecipientListView(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = "mailing_service/mailing_recipient_list.html"
    context_object_name = "mailing_recipient_list"

    def get_queryset(self):
        if (
            self.request.user.has_perm("mailing_service.view_mailingrecipient")
            and self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return get_data_from_cache(model=MailingRecipient)
        return MailingRecipient.objects.filter(owner=self.request.user)


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    template_name = "mailing_service/mailing_recipient_form.html"
    form_class = MailingRecipientForm
    success_url = reverse_lazy("mailing_service:mailing_recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingRecipientDetailView(LoginRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = "mailing_service/mailing_recipient_detail.html"
    context_object_name = "mailing_recipient"

    def get_queryset(self):
        if (
            self.request.user.has_perm("mailing_service.view_mailingrecipient")
            and self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return get_data_from_cache(model=MailingRecipient)
        return MailingRecipient.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.view_mailingrecipient"):
            return HttpResponseForbidden("У вас нет прав для просмотра получателя.")
        return super().dispatch(request, *args, **kwargs)


class MailingRecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingRecipient
    template_name = "mailing_service/mailing_recipient_form.html"
    form_class = MailingRecipientForm
    success_url = reverse_lazy("mailing_service:mailing_recipient_list")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.change_mailingrecipient"):
            return HttpResponseForbidden(
                "У вас нет прав для редактирования получателя."
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.get_object().owner
        return super().form_valid(form)

    def get_queryset(self):
        return MailingRecipient.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "mailing_service:mailing_recipient_detail", args=[self.kwargs["pk"]]
        )


class MailingRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    context_object_name = "mailing_recipient"
    template_name = "mailing_service/mailing_recipient_delete.html"
    success_url = reverse_lazy("mailing_service:mailing_recipient_list")

    def get_queryset(self):
        return MailingRecipient.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.delete_mailingrecipient"):
            return HttpResponseForbidden("У вас нет прав для удаления получателя.")
        return super().dispatch(request, *args, **kwargs)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing_service/message_list.html"
    context_object_name = "message_list"

    def get_queryset(self):
        if (
            self.request.user.has_perm("mailing_service.view_message")
            and self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return get_data_from_cache(model=Message)
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = "mailing_service/message_form.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailing_service:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.view_message"):
            return HttpResponseForbidden("У вас нет прав для просмотра сообщения.")
        return super().dispatch(request, *args, **kwargs)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing_service/message_detail.html"
    context_object_name = "message"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.view_message"):
            return HttpResponseForbidden("У вас нет прав для просмотра сообщения.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if (
            self.request.user.has_perm("mailing_service.view_message")
            and self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return get_data_from_cache(model=Message)
        return Message.objects.filter(owner=self.request.user)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = "mailing_service/message_form.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailing_service:message_list")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.change_message"):
            return HttpResponseForbidden("У вас нет прав для редактирования сообщения.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("mailing_service:message_detail", args=[self.kwargs["pk"]])

    def form_valid(self, form):
        form.instance.owner = self.get_object().owner
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    context_object_name = "message"
    template_name = "mailing_service/message_delete.html"
    success_url = reverse_lazy("mailing_service:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.delete_message"):
            return HttpResponseForbidden("У вас нет прав для удаления сообщения.")
        return super().dispatch(request, *args, **kwargs)


class MailingStatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "mailing_service/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_mailings = Mailing.objects.filter(owner=self.request.user)

        context["total_successful"] = (
            user_mailings.aggregate(Sum("successful_attempts"))[
                "successful_attempts__sum"
            ]
            or 0
        )
        context["total_failed"] = (
            user_mailings.aggregate(Sum("failed_attempts"))["failed_attempts__sum"] or 0
        )
        context["total_messages"] = (
            user_mailings.aggregate(Sum("total_messages_sent"))[
                "total_messages_sent__sum"
            ]
            or 0
        )

        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing_service/mailing_list.html"
    context_object_name = "mailing_list"

    def get_queryset(self):
        if (
            self.request.user.has_perm("mailing_service.view_mailing")
            and self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return get_data_from_cache(model=Mailing)
        return Mailing.objects.filter(owner=self.request.user)

    @staticmethod
    def disable_mailing(request, pk):
        mailing = Mailing.objects.get(pk=pk)
        if not request.user.has_perm("mailing_service.can_disable_mailing"):
            return HttpResponseForbidden("У вас нет прав на отключение рассылки.")

        if mailing.status != "Completed":
            mailing.status = "Completed"
            mailing.end_time = timezone.now()
            mailing.save()

        return redirect(reverse_lazy("mailing_service:mailing_list"))


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = "mailing_service/mailing_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailing_service:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = "Created"
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        recipients_qs = MailingRecipient.objects.filter(owner=self.request.user)
        messages_qs = Message.objects.filter(owner=self.request.user)

        form.fields["recipients"].queryset = recipients_qs
        form.fields["message"].queryset = messages_qs

        return form


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing_service/mailing_detail.html"

    def get_queryset(self):
        if (
            self.request.user.has_perm("mailing_service.view_mailing")
            and self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return get_data_from_cache(model=Mailing)
        return Mailing.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.view_mailing"):
            return HttpResponseForbidden("У вас нет прав для просмотра рассылки.")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        if mailing.status not in ["Running", "Completed"]:
            MailingService.start_mailing(mailing)
        return redirect("mailing_service:mailing_detail", pk=self.kwargs["pk"])


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    template_name = "mailing_service/mailing_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailing_service:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.change_mailing"):
            return HttpResponseForbidden("У вас нет прав для редактирования рассылки.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        recipients_qs = MailingRecipient.objects.filter(owner=self.request.user)
        messages_qs = Message.objects.filter(owner=self.request.user)

        form.fields["recipients"].queryset = recipients_qs
        form.fields["message"].queryset = messages_qs

        return form

    def form_valid(self, form):
        form.instance.owner = self.get_object().owner
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mailing_service:mailing_detail", args=[self.kwargs["pk"]])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    context_object_name = "mailing"
    template_name = "mailing_service/mailing_delete.html"
    success_url = reverse_lazy("mailing_service:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm("mailing_service.delete_mailing"):
            return HttpResponseForbidden("У вас нет прав для удаления рассылки.")
        return super().dispatch(request, *args, **kwargs)
