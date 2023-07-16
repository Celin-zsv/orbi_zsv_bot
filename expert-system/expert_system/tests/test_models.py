import pytest
from data_handler.models import (
    ButtonSlug,
    ButtonUrl,
    Request,
    TelegarmUser,
    Text,
    TextButtonSlug,
    TextButtonUrl,
    UserRequest,
)
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

# All fields of models except m2m fields
# For fields of type ForeignKey, OneToOneField the field name is replaced with the name of the field and the suffix _id
MODEL_FIELDS = [
    [
        # Need more effective way to get fields from AbstractUser
        # These fields are hardcoded here for now
        User,
        [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "confirmation_code",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "password",
        ],
    ],
    [Text, ["id", "text_header", "slug", "text"]],
    [ButtonSlug, ["id", "slug_id", "cover_text"]],
    [ButtonUrl, ["id", "url", "cover_text"]],
    [TelegarmUser, ["id", "user_id"]],
    [Request, ["id", "text_id", "request", "processing_status", "counter", "created_at", "tsv"]],
    [TextButtonSlug, ["id", "button_id", "text_id", "order"]],
    [TextButtonUrl, ["id", "button_id", "text_id", "order"]],
    [UserRequest, ["id", "request_id", "user_id"]],
]
# All m2m fields of models
MODEL_M2M_FIELDS = [[Text, ["button_slug", "button_url"]], [TelegarmUser, ["requests"]]]


def find_verbose_name(fields):
    """Search for a verbose name in a list of fields"""
    for field in fields:
        if field.verbose_name is not None:
            return field
        return None


def model_fields(model_name, expected_fields, fields_type="fields"):
    """Test model fields or m2m fields based on fields_type"""
    if fields_type == "fields":
        model_fields = model_name._meta.fields
    elif fields_type == "m2m_fields":
        model_fields = model_name._meta.many_to_many
    else:
        raise ValueError(f"Invalid fields_type: {fields_type}")
    expected_field_names = set(expected_fields)
    model_field_names = set([field.attname for field in model_fields])
    missing_fields = expected_field_names - model_field_names
    extra_fields = model_field_names - expected_field_names
    assert not missing_fields, f"В модели {model_name} отсутствуют необходимые поля: {missing_fields}"
    assert not extra_fields, f"Найдены лишние поля в модели {model_name}: {extra_fields}"


class TestModels:
    """Test models"""

    @pytest.mark.parametrize("model_name, expected_fields", MODEL_FIELDS)
    def test_model_fields(self, model_name, expected_fields):
        """Each model has specific fields"""
        model_fields(model_name, expected_fields, "fields")

    @pytest.mark.parametrize("model_name, expected_fields", MODEL_M2M_FIELDS)
    def test_model_m2m_fields(self, model_name, expected_fields):
        """Each model has specific m2m fields"""
        model_fields(model_name, expected_fields, "m2m_fields")

    @pytest.mark.parametrize("model_name, test_fields", MODEL_FIELDS)
    def test_fields_verbose_names(self, model_name, test_fields):
        """Each model field has verbose names"""
        for test_field in test_fields:
            field = find_verbose_name(model_name._meta.fields)
            assert field is not None, f"Поле {test_field} в модели {model_name} не имеет атрибута verbose_name"

    @pytest.mark.parametrize("model_class, fields", MODEL_FIELDS)
    def test_model_location_str(self, model_class, fields):
        """Each model has __str__ method"""
        model_instance = model_class()
        model_str_value = str(model_instance)
        assert hasattr(model_instance, "__str__"), f"__str__ метод не найден в модели {model_class}"
        assert model_str_value is not None, f"__str__ метод модели {model_class} возвращает пустое значение"

    @pytest.mark.django_db
    def test_text_button_slug_constraints(self, text_button_slug):
        """TextButtonSlug constraints: can't create two buttons with the same text and button"""
        with pytest.raises(IntegrityError):
            TextButtonSlug.objects.create(text=text_button_slug.text, button=text_button_slug.button)

    @pytest.mark.django_db
    def test_text_button_url_constraints(self, text_button_url):
        """TextButtonUrl constraints: can't create two buttons with the same text and button"""
        with pytest.raises(IntegrityError):
            TextButtonUrl.objects.create(text=text_button_url.text, button=text_button_url.button)

    @pytest.mark.django_db
    def test_user_request_constraints(self, telegram_request):
        """TextButtonUrl constraints: can't create two requests with the same text and user id"""
        with pytest.raises(IntegrityError):
            UserRequest.objects.create(request=telegram_request.request, user=telegram_request.user)

    def test_admin_is_admin(self, admin_user):
        """Admin user has is_admin attribute"""
        assert admin_user.is_admin, "Администратор не имеет атрибута is_admin"

    def test_user_is_not_admin(self, user):
        """User has no is_admin attribute"""
        assert not user.is_admin, "Пользователь имеет атрибут is_admin"
