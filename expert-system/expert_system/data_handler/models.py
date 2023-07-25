from django.contrib.postgres.indexes import BrinIndex, GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from django.db import models
from tinymce import models as tinymce_models

STATUS_CHOICES = (
    ("APPROVED", "Обработан положительно"),
    ("DECLINED", "Обработан отрицательно"),
    ("WAITING", "Не обработан"),
)


class Text(models.Model):
    """Модель для текста."""

    id = models.AutoField(primary_key=True)
    text_header = models.CharField(
        unique=True,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    text = tinymce_models.HTMLField(verbose_name="Текст", help_text="Введите текст", max_length=4096)
    button_slug = models.ManyToManyField("ButtonSlug", through="TextButtonSlug", related_name="button")
    button_url = models.ManyToManyField("ButtonUrl", through="TextButtonUrl", related_name="button")
    is_published = models.BooleanField(
        verbose_name="Опубликован",
        default=True,
        help_text="Текст опубликован /снят с публикации"
    )

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"
        ordering = ("text_header",)

    def __str__(self):
        return self.slug


class BaseButton(models.Model):
    """Базовая модель для кнопок."""

    id = models.AutoField(primary_key=True)
    cover_text = models.CharField(
        max_length=64,
        verbose_name="Текст на кнопке",
        help_text="Введите текст",
    )

    class Meta:
        abstract = True
        ordering = ("cover_text",)

    def __str__(self):
        return self.cover_text


class ButtonSlug(BaseButton):
    slug = models.ForeignKey(
        Text,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Слаг",
        help_text="Выберите слаг текста",
    )

    class Meta(BaseButton.Meta):
        verbose_name = "Кнопка на текст"
        verbose_name_plural = "Кнопки на текст"


class ButtonUrl(BaseButton):
    url = models.URLField(
        verbose_name="Ссылка",
        help_text="Введите ссылку",
    )

    class Meta(BaseButton.Meta):
        verbose_name = "Кнопка на сайт"
        verbose_name_plural = "Кнопки на сайт"


class TelegarmUser(models.Model):
    """Модель для пользователя."""

    id = models.AutoField(primary_key=True)
    user_id = models.CharField(
        unique=True,
        verbose_name="id пользователя",
    )
    requests = models.ManyToManyField("request", through="UserRequest", related_name="requestuser")

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

    def __str__(self):
        return f"Пользователь {self.user_id}"


class Request(models.Model):
    """Модель для запроса."""

    id = models.AutoField(primary_key=True)
    text = models.ForeignKey(
        Text,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="request",
        verbose_name="Текст",
        help_text="Выберите текст для ответа на запрос",
    )
    request = models.TextField(
        verbose_name="Запрос",
        help_text="Введите текст",
    )
    tsv = SearchVectorField(null=True, blank=True, verbose_name="Поисковый вектор")
    processing_status = models.CharField(
        choices=STATUS_CHOICES, max_length=16, verbose_name="Статус обработки", help_text="Выберите статус"
    )
    counter = models.IntegerField(default=1, verbose_name="Счетчик запросов")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания запроса")

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"
        ordering = ("request",)
        indexes = (BrinIndex(fields=["created_at"]), GinIndex(fields=["tsv"]))

    def clean(self):
        if self.processing_status == STATUS_CHOICES[0][0] and self.text is None:
            raise ValidationError('Для запроса в статусе "Обработан положительно" поле Текст должно быть заполнено.')
        if (
            self.processing_status == STATUS_CHOICES[1][0] or self.processing_status == STATUS_CHOICES[2][0]
        ) and self.text is not None:
            raise ValidationError(
                'Для запроса в статусе "Обработан отрицательно" или "Не обработан" поле Текст должно быть пустым.'
            )

    def __str__(self):
        return self.request


class TextButtonSlug(models.Model):
    """Промежуточная модель для кнопок."""

    id = models.AutoField(primary_key=True)
    button = models.ForeignKey(
        ButtonSlug,
        on_delete=models.CASCADE,
        related_name="textslug_list",
        blank=True,
        null=True,
        verbose_name="Кнопка",
        db_index=False,
    )
    text = models.ForeignKey(
        Text,
        on_delete=models.CASCADE,
        related_name="buttonslug_list",
        blank=True,
        null=True,
        verbose_name="Текст",
        db_index=False,
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Порядок кнопки в меню",
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=("button", "text"), name="buttonslug_text_model")]
        verbose_name = "Кнопка на текст"
        verbose_name_plural = "Кнопки на текст"

    def __str__(self):
        return f"{self.button} {self.text}"


class TextButtonUrl(models.Model):
    """Промежуточная модель для кнопок."""

    id = models.AutoField(primary_key=True)
    button = models.ForeignKey(
        ButtonUrl,
        on_delete=models.CASCADE,
        related_name="texturl_list",
        blank=True,
        null=True,
        verbose_name="Кнопка",
        db_index=False,
    )
    text = models.ForeignKey(
        Text,
        on_delete=models.CASCADE,
        related_name="buttonurl_list",
        blank=True,
        null=True,
        verbose_name="Текст",
        db_index=False,
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Порядок кнопки в меню",
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=("button", "text"), name="buttonurl_text_model")]
        verbose_name = "Кнопка на сайт"
        verbose_name_plural = "Кнопки на сайт"

    def __str__(self):
        return f"{self.button} {self.text}"


class UserRequest(models.Model):
    """Промежуточная модель для запросов."""

    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(
        Request,
        on_delete=models.SET_NULL,
        related_name="userrequest",
        blank=True,
        null=True,
        verbose_name="Запрос",
        db_index=False,
    )
    user = models.ForeignKey(
        TelegarmUser,
        on_delete=models.SET_NULL,
        related_name="userrequest",
        blank=True,
        null=True,
        verbose_name="Пользователь",
        db_index=False,
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "request"), name="request_user_model")]
        verbose_name = "Запрос пользователя"
        verbose_name_plural = "Запросы пользователя"

    def __str__(self):
        return f"Запрос '{self.request}' от {self.user}"


class TextButtonSlugArhive(models.Model):
    """Архив моделей: текста, кнопки-на-текст, связи кнопка-текст."""

    id = models.AutoField(primary_key=True)
    button = models.PositiveIntegerField(
        verbose_name="ButtonSlug.id: для восстановления публикации",
        null=False
    )
    text = models.PositiveIntegerField(
        verbose_name="Text.id: для восстановления публикации",
        null=False
    )
    order = models.PositiveSmallIntegerField(
        verbose_name="TextButtonSlug.order: для восстановления публикации",
        null=True
    )

    class Meta:
        verbose_name = "Архив моделей: Кнопка на текст"
        verbose_name_plural = "Архив моделей: Кнопки на текст"

    def __str__(self):
        return f"{self.button} {self.text}"
