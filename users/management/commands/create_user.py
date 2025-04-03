from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    help = "Создаёт пользователя с заданной ролью (менеджер или пользователь)"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Email пользователя")
        parser.add_argument("password", type=str, help="Пароль")
        parser.add_argument(
            "role",
            type=str,
            choices=["user", "manager"],
            help="Роль: 'user' или 'manager'",
        )

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        password = kwargs["password"]
        role = kwargs["role"]

        user, created = CustomUser.objects.get_or_create(email=email)
        if created:
            user.set_password(password)
            user.is_superuser = False
            user.is_staff = False
            user.save()

            group_name = "Менеджеры" if role == "manager" else "Пользователи"
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Пользователь {email} создан с ролью '{group_name}'"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Пользователь {email} уже существует")
            )
