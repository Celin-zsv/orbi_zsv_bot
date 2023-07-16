import pytz
from django.conf import settings


class APITestBase:
    urls = {
        "texts_slug": "/api/texts/{text_slug}/",
        "buttons": "/api/buttons/",
        "requests": "/api/requests/",
        "request_name": "/api/requests/{request_name}/",
        "new_request": "/api/request/",
        "update_request": "/api/request_update/{request_id}/",
        "users": "/api/users/",
        "user_id": "/api/users/{user_id}/",
        "new_user": "/api/user/",
        "update_user": "/api/user_update/{user_id}/",
    }

    def assert_status_code(self, code_expected, response, *args, **kwargs):
        """Assertion to check status code in response"""
        url = kwargs.get("url")
        response_data = ""
        try:
            response_data = response.json()
        except (TypeError, ValueError):
            pass
        assert response.status_code == code_expected, (
            f"При запросе `{url}` со всеми параметрами должен возвращаться "
            f"код {code_expected}, а вернулся код {response.status_code}: {response_data}"
        )
        return response

    def assert_ordered_dict(self, expected, response, *args, **kwargs):
        """Assertion to check ordered dict"""
        key = kwargs.get("key")
        url = kwargs.get("url")
        # assert len(response) == len(expected)
        for i in range(len(expected)):
            response_dict = dict(response[i])
            assert (
                response_dict == expected[i]
            ), f"На странице {url} значение поля {key} не совпадает, ожидалось {expected[i]}, получено {response_dict}"

    def formatted_datetime(self, datetime_string):
        """Return formatted datetime string"""
        desired_timezone = pytz.timezone(settings.TIME_ZONE)
        formatted_datetime = datetime_string.astimezone(desired_timezone).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        return formatted_datetime[:-2] + ":" + formatted_datetime[-2:]
