import os
from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()


@pytest.mark.django_db
class TestCommands:
    """Test management commands for the expert_system app."""

    def test_existing_user_with_regenerate(
        self, regenerate_flag, bot_username, bot_password, existing_bot_user, token, capfd
    ):
        """Test bot_token command with existing user and regenerate flag."""
        with mock.patch.dict(os.environ, {"BOT_USERNAME": bot_username, "BOT_PASSWORD": bot_password}):
            call_command("bot_token", "--regenerate")

        out, _ = capfd.readouterr()
        assert f"Служебная учетная запись для бота '{bot_username}' уже создана." in out
        assert "Сгенерирован новый токен" in out

    def test_existing_user_without_regenerate(self, bot_username, bot_password, existing_bot_user, token, capfd):
        """Test bot_token command with existing user and without regenerate flag."""
        with mock.patch.dict(os.environ, {"BOT_USERNAME": bot_username, "BOT_PASSWORD": bot_password}):
            call_command("bot_token")

        out, _ = capfd.readouterr()
        assert f"Токен для служебной учетной записи бота '{bot_username}' уже существует." in out

    def test_new_user_with_regen(self, regenerate_flag, bot_username, bot_password, capfd):
        """Test bot_token command with new user and regenerate flag."""
        with mock.patch.dict(os.environ, {"BOT_USERNAME": bot_username, "BOT_PASSWORD": bot_password}):
            call_command("bot_token", "--regenerate")

        out, _ = capfd.readouterr()
        assert f"Создана служебная учетная запись для бота '{bot_username}' и токен:" in out

    def test_nonexistent_user(self, bot_username, bot_password, capfd):
        """Test bot_token command with nonexistent user."""
        with mock.patch.dict(os.environ, {"BOT_USERNAME": bot_username, "BOT_PASSWORD": bot_password}):
            call_command("bot_token")

        out, _ = capfd.readouterr()
        assert f"Создана служебная учетная запись для бота '{bot_username}' и токен:" in out
