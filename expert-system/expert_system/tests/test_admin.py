from http import HTTPStatus

import pytest
from data_handler.admin_forms import RequestForm
from data_handler.models import Request, TelegarmUser
from django.urls import reverse


class TestAdminSite:
    """Admin site tests"""

    def make_url(self, model, page, id=None):
        """Make reverse url for admin page"""
        url = f"admin:{model._meta.app_label}_{model._meta.model_name}_{page}"
        if id is not None:
            return reverse(url, args=(id,))
        return reverse(url)

    @pytest.mark.parametrize("model", (TelegarmUser,))
    def test_add(self, model, admin_user, django_admin_client):
        """Forbidden add action on admin site"""
        url = self.make_url(model, "add")
        response = django_admin_client.post(url)
        assert response.status_code == HTTPStatus.FORBIDDEN

    @pytest.mark.parametrize("action, model", (("delete", TelegarmUser), ("change", TelegarmUser)))
    def test_delete(self, action, model, admin_user, django_admin_client, telegram_user):
        """Forbidden change and delete actions on admin site"""
        url = self.make_url(model, action, id=telegram_user.id)
        response = django_admin_client.post(url)
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_readonly_telegram_request(self, admin_user, django_admin_client, telegram_request):
        """Readonly telegram request on admin site"""
        url = self.make_url(Request, "change", id=telegram_request.id)
        response = django_admin_client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert (
            "request" in response.context_data["adminform"].readonly_fields
        ), "Поле request должно быть только для чтения для запросов переданных из телеграма"

    def test_editable_request(self, admin_user, django_admin_client, request1):
        """Editable request on admin site"""
        url = self.make_url(Request, "change", id=request1.id)
        response = django_admin_client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert (
            "request" not in response.context_data["adminform"].readonly_fields
        ), "Поле request должно быть редактируемым для запросов созданных в админке"

    @pytest.mark.django_db()
    def test_request_case_sensitive(self, request1):
        """Request case sensitive on admin site"""
        form = RequestForm({"request": "test request"})
        assert not form.is_valid()
        assert "request" in form.errors
        assert str(form.errors["request"][0]) == "Такой запрос уже существует"
