import pytest
from data_handler.models import (
    STATUS_CHOICES,
    ButtonSlug,
    ButtonUrl,
    Request,
    TelegarmUser,
    Text,
    TextButtonSlug,
    TextButtonUrl,
    UserRequest,
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def user(django_user_model):
    """Regular user fixture"""
    return django_user_model.objects.create_user(
        username="test-user",
        first_name="Tester",
        last_name="Testerson",
        email="test.user@fake.mail",
        password="12345Qq",
        is_active=True,
        role=settings.USER,
    )


@pytest.fixture
def admin(django_user_model):
    """Admin user fixture"""
    return django_user_model.objects.create_user(
        username="test-admin",
        first_name="Tester",
        last_name="Testerson",
        email="test.admin@fake.mail",
        password="12345Qq",
        is_active=True,
        role=settings.ADMIN,
        is_superuser=True,
        is_staff=True,
    )


@pytest.fixture
def user_client(user):
    """Regular user http-client fixture"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_client(admin):
    """Admin http-client fixture"""
    client = APIClient()
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def django_admin_client(admin):
    client = Client()
    client.force_login(admin)
    return client


@pytest.fixture
def button_slug(text):
    """ButtonSlug fixture with is_main=False"""
    button_slug = ButtonSlug.objects.create(cover_text="Button")
    button_slug.slug = text
    button_slug.save()
    return button_slug


@pytest.fixture
def button_url():
    """ButtonUrl fixture"""
    return ButtonUrl.objects.create(url="https://test.url", cover_text="URL Button")


@pytest.fixture
def text_button_slug(text, button_slug):
    return TextButtonSlug.objects.create(text=text, button=button_slug, order=1)


@pytest.fixture
def text_button_url(text, button_url):
    return TextButtonUrl.objects.create(text=text, button=button_url, order=1)


@pytest.fixture
def text():
    """Text fixture"""
    return Text.objects.create(text_header="Test text header", slug="test-text", text="Test text Test text")


@pytest.fixture
def text_with_buttons(text, button_slug, button_url):
    """Text fixture with buttons"""
    text.button_slug.add(button_slug)
    text.button_url.add(button_url)
    return text


@pytest.fixture
def request1(text):
    """Request fixture"""
    return Request.objects.create(request="Test request", text=text)


@pytest.fixture
def request2(text):
    """Another Request fixture"""
    return Request.objects.create(
        request="Another test request",
        text=text,
        processing_status=STATUS_CHOICES[1][0],
    )


@pytest.fixture
def request3(request, text):
    """Request fixture"""
    return Request.objects.create(
        request=request.param,
        text=text,
        processing_status=STATUS_CHOICES[0][0],
    )


@pytest.fixture
def telegram_user():
    """TelegramUser with request fixture"""
    return TelegarmUser.objects.create(user_id=123456789)


@pytest.fixture
def telegram_request(telegram_user, request1):
    """UserRequest fixture"""
    return UserRequest.objects.create(request=request1, user=telegram_user)


@pytest.fixture
def bot_username():
    """Telegram bot service account username"""
    return "test_bot_username"


@pytest.fixture
def bot_password():
    """Telegram bot service account password"""
    return "test_bot_password"


@pytest.fixture
def existing_bot_user(bot_username, bot_password):
    """Telegram bot service account user"""
    return User.objects.create_user(username=bot_username, password=bot_password)


@pytest.fixture
def token(existing_bot_user):
    """Telegram bot service account token"""
    return Token.objects.create(user=existing_bot_user)


@pytest.fixture
def regenerate_flag():
    """Flag for regenerating token"""
    return True
