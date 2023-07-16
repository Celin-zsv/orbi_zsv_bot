from data_handler.views import Buttons, RequestList, RequestPatch, RequestRetrieve, TextSlug, User, UserList
from django.urls import path

urlpatterns = [
    # Получить текст по его slug
    path("texts/<slug:slug>/", TextSlug.as_view(), name="texts_slug"),
    # Получить все кнопки
    path("buttons/", Buttons.as_view(), name="buttons"),
    # Получить все запросы
    path("requests/", RequestList.as_view(), name="requests"),
    # Получить запрос по его тексту
    path("requests/<str:name>/", RequestRetrieve.as_view(), name="request_name"),
    # Создать запрос
    path("request/", RequestList.as_view(), name="new_request"),
    # Увеличить счетчик запроса на 1
    path("request_update/<int:request_id>/", RequestPatch.as_view(), name="update_request"),
    # Получить всех пользователей
    path("users/", UserList.as_view(), name="users"),
    # Получить пользователя по его user_id
    path("users/<int:user_id>/", User.as_view(), name="user_id"),
    # Создать пользователя
    path("user/", UserList.as_view(), name="new_user"),
    # Редактор запросов пользователя
    path("user_update/<int:user_id>/", User.as_view(), name="update_user"),
]
