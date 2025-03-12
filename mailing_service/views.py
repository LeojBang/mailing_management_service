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


class MailingRecipientListView(ListView):
    model = MailingRecipient
    template_name = 'mailing_service/mailing_recipient_list.html'
    context_object_name = 'mailing_recipient_list'


class MailingRecipientCreateView(CreateView):
    model = MailingRecipient
    template_name = 'mailing_service/mailing_recipient_form.html'
    form_class = MailingRecipientForm
    success_url = reverse_lazy('mailing_service:mailing_recipient_list')


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient
    template_name = 'mailing_service/mailing_recipient_detail.html'
    context_object_name = 'mailing_recipient'


class MailingRecipientUpdateView(UpdateView):
    model = MailingRecipient
    template_name = 'mailing_service/mailing_recipient_form.html'
    form_class = MailingRecipientForm
    success_url = reverse_lazy('mailing_service:mailing_recipient_list')

    def get_success_url(self):
        return reverse_lazy('mailing_service:mailing_recipient_detail', args=[self.kwargs["pk"]])


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    context_object_name = 'mailing_recipient'
    template_name = 'mailing_service/mailing_recipient_delete.html'
    success_url = reverse_lazy('mailing_service:mailing_recipient_list')


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


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_service/mailing_list.html'
    context_object_name = 'mailing_list'

    def get_queryset(self):
        return Mailing.objects.prefetch_related('recipients')


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailing_service/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing_service:mailing_list')


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_service/mailing_detail.html'

    def get_queryset(self):
        return Mailing.objects.prefetch_related('recipients')


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing_service/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing_service:mailing_list')

    def get_success_url(self):
        return reverse_lazy('mailing_service:mailing_detail', args=[self.kwargs["pk"]])


class MailingDeleteView(DeleteView):
    model = Mailing
    context_object_name = 'mailing'
    template_name = 'mailing_service/mailing_delete.html'
    success_url = reverse_lazy('mailing_service:mailing_list')
