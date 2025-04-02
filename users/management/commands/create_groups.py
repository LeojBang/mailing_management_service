from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.models import CustomUser  # Убедитесь, что путь к модели корректный


class Command(BaseCommand):
    help = "Создаёт группы 'Менеджеры' и 'Пользователи' с необходимыми правами"

    def handle(self, *args, **options):
        # Создаём или получаем группу "Пользователи"
        user_group, created = Group.objects.get_or_create(name="Пользователи")
        user_permissions = [
            "add_mailing", "view_mailing", "change_mailing", "delete_mailing",
            "add_mailingrecipient", "view_mailingrecipient", "change_mailingrecipient", "delete_mailingrecipient",
            "add_message", "view_message", "change_message", "delete_message",
        ]
        for perm in user_permissions:
            permission = Permission.objects.get(codename=perm)
            user_group.permissions.add(permission)

        # Создаём или получаем группу "Менеджеры"
        manager_group, created = Group.objects.get_or_create(name="Менеджеры")
        manager_permissions = [
            "view_mailing", "view_mailingrecipient", "view_message",
            "can_disable_mailing", "can_block_user"
        ]
        for perm in manager_permissions:
            permission = Permission.objects.get(codename=perm)
            manager_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS("Группы 'Менеджеры' и 'Пользователи' успешно созданы!"))