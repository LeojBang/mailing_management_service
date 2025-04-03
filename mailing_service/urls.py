from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_service.apps import MailingServiceConfig
from mailing_service.views import (
    HomeView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingRecipientCreateView,
    MailingRecipientDeleteView,
    MailingRecipientDetailView,
    MailingRecipientListView,
    MailingRecipientUpdateView,
    MailingStatisticsView,
    MailingUpdateView,
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
)

app_name = MailingServiceConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "mailing_recipient/",
        cache_page(300)(MailingRecipientListView.as_view()),
        name="mailing_recipient_list",
    ),
    path(
        "mailing_recipient/create/",
        MailingRecipientCreateView.as_view(),
        name="mailing_recipient_create",
    ),
    path(
        "mailing_recipient/<int:pk>/",
        cache_page(300)(MailingRecipientDetailView.as_view()),
        name="mailing_recipient_detail",
    ),
    path(
        "mailing_recipient/<int:pk>/update/",
        MailingRecipientUpdateView.as_view(),
        name="mailing_recipient_update",
    ),
    path(
        "mailing_recipient/<int:pk>/delete/",
        MailingRecipientDeleteView.as_view(),
        name="mailing_recipient_delete",
    ),
    path("message/", cache_page(300)(MessageListView.as_view()), name="message_list"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path(
        "message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailing/", cache_page(300)(MailingListView.as_view()), name="mailing_list"),
    path("statistics/", MailingStatisticsView.as_view(), name="mailing_statistics"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing/<int:pk>/",
        cache_page(300)(MailingDetailView.as_view()),
        name="mailing_detail",
    ),
    path(
        "mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
]
