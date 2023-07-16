from django.core.management.base import BaseCommand, CommandError
from expert_system.utils import find_closest_request, timeit


class Command(BaseCommand):
    help = "Поиск самого похожего запроса в базе данных"

    def add_arguments(self, parser):
        parser.add_argument("user_request", type=str, help="Пользовательский запрос")

    @timeit
    def handle(self, *args, **options):
        closest_request = find_closest_request(options["user_request"])
        if closest_request is None:
            raise CommandError("Не удалось найти похожий запрос")
        self.stdout.write(
            self.style.SUCCESS(
                f'Наиболее похожий запрос на "{options["user_request"]}" - "{closest_request.request}" и '
                f'ответ: "{closest_request.text.text}".'
            )
        )
