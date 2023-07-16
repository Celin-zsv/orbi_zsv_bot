import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

User = get_user_model()


class Command(BaseCommand):
    help = "Генерирует специальный токен для бота."

    def add_arguments(self, parser):
        parser.add_argument(
            "-r",
            "--regenerate",
            action="store_true",
            help="Регенерировать токен для существующей служебной учетной записи бота.",
        )

    def handle(self, *args, **options):
        bot_username = os.getenv("BOT_USERNAME", default="bot_username")
        bot_password = os.getenv("BOT_PASSWORD", default="bot_password")
        regenerate_token = options.get("regenerate")

        try:
            user = User.objects.get(username=bot_username)
            if regenerate_token:
                # Delete the existing token
                Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(
                    f"Служебная учетная запись для бота '{bot_username}' уже создана. "
                    f"Сгенерирован новый токен\n{token.key}"
                )
            else:
                self.stdout.write(
                    f"Токен для служебной учетной записи бота '{bot_username}' уже существует. Токен:\n{token.key}"
                )
        except User.DoesNotExist:
            user = User.objects.create_user(username=bot_username, password=bot_password)
            token = Token.objects.create(user=user)
            self.stdout.write(f"Создана служебная учетная запись для бота '{bot_username}' и токен:\n{token.key}")
