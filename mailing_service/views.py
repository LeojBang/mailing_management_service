from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView

from mailing_service.forms import MailingRecipientForm, MessageForm, MailingForm
from mailing_service.models import MailingRecipient, Message, Mailing


# Create your views here.
class HomeView(TemplateView):
    template_name = 'mailing_service/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_count = Mailing.objects.all().count()
        mailing_count_active = Mailing.objects.filter(status='Running').count()
        mailing_recipient_count = MailingRecipient.objects.count()
        context['mailing_count'] = mailing_count
        context['mailing_count_active'] = mailing_count_active
        context['mailing_recipient_count'] = mailing_recipient_count
        return context


class MailingRecipientListView(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = 'mailing_service/mailing_recipient_list.html'
    context_object_name = 'mailing_recipient_list'

    def get_queryset(self):
        return MailingRecipient.objects.filter(owner=self.request.user)


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    template_name = 'mailing_service/mailing_recipient_form.html'
    form_class = MailingRecipientForm
    success_url = reverse_lazy('mailing_service:mailing_recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient
    template_name = 'mailing_service/mailing_recipient_detail.html'
    context_object_name = 'mailing_recipient'


class MailingRecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingRecipient
    template_name = 'mailing_service/mailing_recipient_form.html'
    form_class = MailingRecipientForm
    success_url = reverse_lazy('mailing_service:mailing_recipient_list')

    def get_queryset(self):
        return MailingRecipient.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('mailing_service:mailing_recipient_detail', args=[self.kwargs["pk"]])


class MailingRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    context_object_name = 'mailing_recipient'
    template_name = 'mailing_service/mailing_recipient_delete.html'
    success_url = reverse_lazy('mailing_service:mailing_recipient_list')

    def get_queryset(self):
        return MailingRecipient.objects.filter(owner=self.request.user)


class MessageListView(ListView):
    model = Message
    template_name = 'mailing_service/message_list.html'
    context_object_name = 'message_list'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'mailing_service/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:message_list')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing_service/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailing_service/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:message_list')

    def get_success_url(self):
        return reverse_lazy('mailing_service:message_detail', args=[self.kwargs["pk"]])


class MessageDeleteView(DeleteView):
    model = Message
    context_object_name = 'message'
    template_name = 'mailing_service/message_delete.html'
    success_url = reverse_lazy('mailing_service:message_list')


class MailingStatisticsView(TemplateView):
    template_name = "mailing_service/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_mailings = Mailing.objects.filter(owner=self.request.user)

        context["total_successful"] = user_mailings.aggregate(Sum("successful_attempts"))[
                                          "successful_attempts__sum"] or 0
        context["total_failed"] = user_mailings.aggregate(Sum("failed_attempts"))["failed_attempts__sum"] or 0
        context["total_messages"] = user_mailings.aggregate(Sum("total_messages_sent"))["total_messages_sent__sum"] or 0

        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_service/mailing_list.html'
    context_object_name = 'mailing_list'

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, имеет ли пользователь право на просмотр списка клиентов
        if not request.user.has_perm("mailings.view_mailing"):
            return HttpResponseForbidden(
                "У вас нет прав для просмотра списка рассылок."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.has_perm("mailings.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = 'mailing_service/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing_service:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_service/mailing_detail.html'

    def get_queryset(self):
        return Mailing.objects.prefetch_related('recipients')


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    template_name = 'mailing_service/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing_service:mailing_list')
    permission_required = "mailings.can_disable_mailing"

    def get_queryset(self):
        if self.request.user.has_perm("mailings.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('mailing_service:mailing_detail', args=[self.kwargs["pk"]])


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    context_object_name = 'mailing'
    template_name = 'mailing_service/mailing_delete.html'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def get_queryset(self):
        if self.request.user.has_perm("mailings.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)
