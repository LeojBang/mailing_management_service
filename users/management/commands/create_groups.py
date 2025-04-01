from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Create moderator group with permissions"

    def handle(self, *args, **options):
        # Создаем группу
        group, created = Group.objects.get_or_create(name="Менеджеры")

        # Добавляем разрешения
        unpublish_perm = Permission.objects.get(codename="can_unpublish_product")
        delete_perm = Permission.objects.get(codename="delete_product")
        group.permissions.add(unpublish_perm, delete_perm)

        group.save()
        self.stdout.write(self.style.SUCCESS("Группа модераторов создана"))
