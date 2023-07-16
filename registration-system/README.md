# Сервис обработки регистраций

## Подготовка

### 1. Установка poetry и запуск виртауального окружения
Важно: poetry ставится и запускается для каждого сервиса отдельно.

1. Перейти в папку сервиса:
```bash
cd registration-system
```
2. Затем выполните команды:

Для Linux, macOS, Windows (WSL):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Для Windows (Powershell):
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
Альтернативная команда для Windows (Powershell):
```bash
pip install poetry
```
Чтобы скрипты выполнялись, PowerShell может попросить у вас поменять политики.

В macOS и Windows сценарий установки предложит добавить папку с исполняемым файлом poetry в переменную PATH. Сделайте это, выполнив следующую команду:

macOS (не забудьте поменять jetbrains на имя вашего пользователя)
```bash
export PATH="/Users/jetbrains/.local/bin:$PATH"
```

Windows
```bash
$Env:Path += ";C:\Users\jetbrains\AppData\Roaming\Python\Scripts"; setx PATH "$Env:Path"
```

Для проверки установки выполните следующую команду:
```bash
poetry --version
```

Создание виртуально окружения
```bash
poetry env use python3.10
```
или
```bash
poetry env use python3
```

Установка зависимостей (для разработки)
```bash
poetry install --with dev
```

Запуск оболочки и активация виртуального окружения

```bash
your@device:~/your_project_pwd/your_service$ poetry shell
```

Проверка активации виртуального окружения
```bash
poetry env list
```


* Полная документация: https://python-poetry.org/docs/#installation


### 2. Запуск сервиса

1. Перейти в папку сервиса:
```bash
cd registration-system
```

2. Сделать миграции:
```bash
poetry run task makemigrations
poetry run task migrate
```

3. Выполнить команду:
```bash
poetry run task start
```

## Запуск Celery+FastAPI

1. Запуск брокера сообщений в docker
```bash
poetry run docker run -d --name some-rabbit -p 4369:4369 -p 5671:5671 -p 5672:5672 -p 15672:15672 rabbitmq:3
```
или
```bash
poetry run task rabbitmq
```


**Далее каждую команду нужно запускать в отдельном экземпляре терминала**
2. Запуск FastAPI
```bash
poetry run uvicorn app.main:app --reload
```
или
```bash
poetry run task start
```

По адресу http://127.0.0.1:8000/docs#/
Функция registration/{period}, копия функции registration
с эмуляцией медленных процессов. {period} время задержки в секундах
*до запуска Celery управление возвращается через заданноее время*
3. Запуск Celery

Windows

```bash
poetry run celery_windows
```

Linux

```bash
poetry run celery -A app.celery_worker.celery worker --loglevel=info
```
или
```bash
poetry run task celery
```

4. Запуск Flower - сервер мониторинга очереди задач
```bash
poetry run celery -A app.celery_worker.celery flower --broker:amqp://localhost//
```
или
```bash
poetry run task flower
```

Теперь по адресу http://127.0.0.1:8000/docs#/
Функция registration/{period} возвращает управление
По адресу http://127.0.0.1:5555/ можно отслеживать очередь задач

### Запуск тестов
Важно: должен быть запущен контейнер db_registration.

1. Перейти в папку сервиса:
```bash
cd registration-system
```

2. Запустить тесты
```bash
pytest
```
