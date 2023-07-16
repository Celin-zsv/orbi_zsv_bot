# Сервис эксперт-системы

## Запуск сервиса

1. Активируем виртуальное окружение
2. Устанавливаем зависимости
3. Запускаем базу данных
4. Создаём миграции
```bash
poetry run task makemigrations
```

5. Применяем миграции:
```bash
poetry run task migrate
```
6. Скачиваем данные для библиотеки nltk (достаточно сделать 1 раз при первом запуске сервиса, затем шаг можно пропускать)
```bash
poetry run task download_nltk
```

7. При необходимости создаём суперюзера, если он не был создан:

```bash
poetry run task createsuperuser
```
8. Создаём токен для доступа к API
```bash
poetry run task bot_token
```
9. Запускаем приложение
```bash
poetry run task start
```

Ссылка на сервис: http://127.0.0.1:8000/admin/

## Запуск тестов

Сервис покрыт тестами,
[смотрите инструкции о системе тестирования](https://github.com/orbifond/orbi_bot/blob/8ca2dd787edc60dd2f86da5cc5437b486e6fb11d/expert-system/expert_system/tests/README.md)
сервиса и о вариантах запуска на отдельной странице.
