from http import HTTPStatus
from urllib.parse import quote

import pytest
from data_handler.models import Request, TelegarmUser

from tests.common import APITestBase


class TestAPI(APITestBase):
    """Test API"""

    @pytest.mark.parametrize("url_key, expected_url", APITestBase.urls.items())
    @pytest.mark.parametrize("user_client", [True, False], indirect=True, ids=["User Client", "Anon Client"])
    def test_urls_availability(self, url_key, expected_url, user_client, telegram_user, text, button_slug, request1):
        """URLs available for authorized user"""
        url = expected_url.format(
            text_slug=text.slug,
            request_name=request1.request,
            request_id=request1.id,
            user_id=telegram_user.user_id,
        )
        try:
            response = user_client.get(url) if user_client else self.client.get(url)
        except Exception as error:
            assert False, f"При запросе на `{url}` возникла ошибка: {error}"

        if user_client:
            assert (
                response.status_code != HTTPStatus.NOT_FOUND
            ), f"Адрес {url} не найден, проверьте этот адрес в urls.py"
        else:
            assert (
                response.status_code == HTTPStatus.UNAUTHORIZED
            ), f"Адрес {url} доступен для неавторизованного пользователя"

    def test_get_buttons_list(self, user_client, button_slug, button_url):
        """Endpoint /api/buttons/ should return buttons list"""
        url = APITestBase.urls["buttons"]
        response = user_client.get(url)
        self.assert_status_code(HTTPStatus.OK, response, url=url)
        expected_fields = {
            "ButtonSlug": [{"id": button_slug.id, "cover_text": button_slug.cover_text, "slug": button_slug.slug.slug}],
            "ButtonUrl": [{"id": button_url.id, "cover_text": button_url.cover_text, "url": button_url.url}],
        }
        for key, value in expected_fields.items():
            self.assert_ordered_dict(value, response.data[key], key=key, url=url)

    @pytest.mark.parametrize("url_key", ("requests", "request_name"))
    def test_get_requests(self, user_client, request1, url_key):
        """Endpoint /api/requests/ should return requests list"""
        url = APITestBase.urls[url_key].format(request_name=request1.request)
        response = user_client.get(url)
        self.assert_status_code(HTTPStatus.OK, response, url=url)
        expected_fields = {
            "id": request1.id,
            "request": request1.request,
            "text": {
                "id": request1.text.id,
                "button_slug": [],
                "button_url": [],
                "text_header": request1.text.text_header,
                "slug": request1.text.slug,
                "text": request1.text.text,
            },
            "processing_status": request1.processing_status,
            "counter": request1.counter,
            "created_at": self.formatted_datetime(request1.created_at),
            "requestuser": [],
        }
        for key, value in expected_fields.items():
            if url_key == "requests":
                response_data = response.data[0][key]
            else:
                response_data = response.data[key]
            assert (
                response_data == value
            ), f"Значение поля {key} не совпадает, ожидалось {value}, получено {response_data}"

    def test_request_404(self, user_client, request1):
        """Endpoint /api/requests/ should return 404 if request not found"""
        url = APITestBase.urls["request_name"].format(request_name="Something wrong")
        response = user_client.get(url)
        self.assert_status_code(HTTPStatus.NOT_FOUND, response, url=url)

    @pytest.mark.parametrize(
        "request3",
        [
            "test test?",
            "test ? test ? id1 & name2",
            "Sample text with Russian symbols: Привет, мир!",
            "Text with digits: 12345",
            "Text with special symbols: !@#$%^&*()",
        ],
        indirect=True,
    )
    def test_get_requests_detail(self, user_client, request3):
        """Endpoint /api/requests/ should return request detail when request name contains strange symbols"""
        url = quote(APITestBase.urls["request_name"].format(request_name=request3.request))
        response = user_client.get(url)
        self.assert_status_code(HTTPStatus.OK, response, url=url)

    @pytest.mark.parametrize("url_key", ("users", "user_id"))
    def test_get_users(self, user_client, telegram_user, url_key):
        """Endpoint /api/users/ should return users list"""
        url = APITestBase.urls[url_key].format(user_id=telegram_user.user_id)
        response = user_client.get(url)
        self.assert_status_code(HTTPStatus.OK, response, url=url)
        expected_fields = {"id": telegram_user.id, "user_id": str(telegram_user.user_id), "requests": []}
        for key, value in expected_fields.items():
            if url_key == "users":
                response_data = response.data[0][key]
            else:
                response_data = response.data[key]
            assert (
                response_data == value
            ), f"Значение поля {key} не совпадает, ожидалось {value}, получено {response_data}"

    def test_create_request(self, user_client):
        """Endpoint /api/requests/ should create request"""
        # Delete all objects from the DB to be sure that there's only one object after POST request
        Request.objects.all().delete()
        url = APITestBase.urls["requests"]
        data = {"request": "test", "processing_status": "WAITING"}
        response = user_client.post(url, data=data)
        self.assert_status_code(HTTPStatus.CREATED, response, url=url)
        assert Request.objects.count() == 1, "Объект должен быть добавлен в БД и не должен дублироваться"
        stored_request = Request.objects.first()
        assert stored_request.request == data["request"], "Значение поля request не совпадает"
        assert (
            stored_request.processing_status == data["processing_status"]
        ), "Значение поля processing_status не совпадает"

    def test_create_double_request(self, user_client, request2):
        """Endpoint /api/requests/ should return 400 if request already exists"""
        url = APITestBase.urls["requests"]
        data = {"request": request2.request, "processing_status": request2.processing_status}
        response = user_client.post(url, data=data)
        self.assert_status_code(HTTPStatus.BAD_REQUEST, response, url=url)
        assert Request.objects.count() == 1, "Объект не должен быть добавлен в БД"
        assert response.data["non_field_errors"][0] == "This object already exists"

    def test_create_wrong_request(self, user_client):
        """Endpoint /api/requests/ should return 400 if request is empty"""
        url = APITestBase.urls["requests"]
        data = {"request": "", "processing_status": "WAITING"}
        response = user_client.post(url, data=data)
        self.assert_status_code(HTTPStatus.BAD_REQUEST, response, url=url)
        data = {"request": "test", "processing_status": ""}
        response = user_client.post(url, data=data)
        self.assert_status_code(HTTPStatus.BAD_REQUEST, response, url=url)

    def test_update_request_counter(self, user_client, request1):
        """Endpoint /api/requests/ should update request counter"""
        counter = request1.counter
        url = APITestBase.urls["update_request"].format(request_id=request1.id)
        response = user_client.patch(url)
        self.assert_status_code(HTTPStatus.OK, response, url=url)
        assert response.data["counter"] == counter + 1, "Значение поля counter должно быть увеличено на 1"

    def test_update_wrong_request(self, user_client):
        """Endpoint /api/requests/ should return HTTPStatus.NOT_FOUND if request doesn't exist"""
        url = APITestBase.urls["update_request"].format(request_id=999_999)
        response = user_client.patch(url)
        self.assert_status_code(HTTPStatus.NOT_FOUND, response, url=url)

    def test_create_tg_user(self, user_client):
        """Endpoint /api/users/ should create telegram user"""
        # Delete all objects from the DB to be sure that there's only one object after POST request
        TelegarmUser.objects.all().delete()
        url = APITestBase.urls["new_user"]
        data = {"user_id": "123456789"}
        response = user_client.post(url, data=data)
        self.assert_status_code(HTTPStatus.CREATED, response, url=url)
        assert TelegarmUser.objects.count() == 1, "Объект должен быть добавлен в БД и не должен дублироваться"
        stored_user = TelegarmUser.objects.first()
        assert stored_user.user_id == data["user_id"], "Значение поля user_id не совпадает"

    def test_create_double_tg_user(self, user_client, telegram_user):
        """Endpoint /api/users/ should return HTTPStatus.BAD_REQUEST if user already exists"""
        url = APITestBase.urls["new_user"]
        data = {"user_id": telegram_user.user_id}
        response = user_client.post(url, data=data)
        self.assert_status_code(HTTPStatus.BAD_REQUEST, response, url=url)
        assert TelegarmUser.objects.count() == 1, "Объект не должен быть добавлен в БД"
