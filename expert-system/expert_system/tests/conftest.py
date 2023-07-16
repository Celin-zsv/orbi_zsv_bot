from pathlib import Path

from django.utils.version import get_version

PROJECT_DIR = Path(__file__).resolve().parent.parent
APP_DIRS = ["api", "data_handler", "expert_system", "users"]

assert get_version() > "4.1.7", "Пожалуйста, используйте версию Django > 4.1.7"

for app_dir in APP_DIRS:
    if not Path(PROJECT_DIR / app_dir).is_dir():
        assert False, f"В папке проекта {PROJECT_DIR} не найдено директории приложения {app_dir}"

pytest_plugins = ["tests.fixtures.fixtures_data"]
