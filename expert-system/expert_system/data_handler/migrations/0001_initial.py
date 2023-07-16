# Generated by Django 4.2.2 on 2023-07-06 15:44

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ButtonSlug",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "cover_text",
                    models.CharField(
                        help_text="Введите текст",
                        max_length=64,
                        verbose_name="Текст на кнопке",
                    ),
                ),
            ],
            options={
                "verbose_name": "Кнопка на текст",
                "verbose_name_plural": "Кнопки на текст",
                "ordering": ("cover_text",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ButtonUrl",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "cover_text",
                    models.CharField(
                        help_text="Введите текст",
                        max_length=64,
                        verbose_name="Текст на кнопке",
                    ),
                ),
                (
                    "url",
                    models.URLField(help_text="Введите ссылку", verbose_name="Ссылка"),
                ),
            ],
            options={
                "verbose_name": "Кнопка на сайт",
                "verbose_name_plural": "Кнопки на сайт",
                "ordering": ("cover_text",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Request",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "request",
                    models.TextField(help_text="Введите текст", verbose_name="Запрос"),
                ),
                (
                    "tsv",
                    django.contrib.postgres.search.SearchVectorField(
                        blank=True, null=True, verbose_name="Поисковый вектор"
                    ),
                ),
                (
                    "processing_status",
                    models.CharField(
                        choices=[
                            ("APPROVED", "Обработан положительно"),
                            ("DECLINED", "Обработан отрицательно"),
                            ("WAITING", "Не обработан"),
                        ],
                        help_text="Выберите статус",
                        max_length=16,
                        verbose_name="Статус обработки",
                    ),
                ),
                (
                    "counter",
                    models.IntegerField(default=1, verbose_name="Счетчик запросов"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания запроса"
                    ),
                ),
            ],
            options={
                "verbose_name": "Запрос",
                "verbose_name_plural": "Запросы",
                "ordering": ("request",),
            },
        ),
        migrations.CreateModel(
            name="TelegarmUser",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "user_id",
                    models.CharField(unique=True, verbose_name="id пользователя"),
                ),
            ],
            options={
                "verbose_name": "Пользователь Telegram",
                "verbose_name_plural": "Пользователи Telegram",
            },
        ),
        migrations.CreateModel(
            name="Text",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "text_header",
                    models.CharField(
                        help_text="Введите заголовок",
                        unique=True,
                        verbose_name="Заголовок",
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Слаг")),
                (
                    "text",
                    tinymce.models.HTMLField(
                        help_text="Введите текст", max_length=4096, verbose_name="Текст"
                    ),
                ),
            ],
            options={
                "verbose_name": "Текст",
                "verbose_name_plural": "Тексты",
                "ordering": ("text_header",),
            },
        ),
        migrations.CreateModel(
            name="UserRequest",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "request",
                    models.ForeignKey(
                        blank=True,
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="userrequest",
                        to="data_handler.request",
                        verbose_name="Запрос",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="userrequest",
                        to="data_handler.telegarmuser",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Запрос пользователя",
                "verbose_name_plural": "Запросы пользователя",
            },
        ),
        migrations.CreateModel(
            name="TextButtonUrl",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Порядок кнопки в меню"
                    ),
                ),
                (
                    "button",
                    models.ForeignKey(
                        blank=True,
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="texturl_list",
                        to="data_handler.buttonurl",
                        verbose_name="Кнопка",
                    ),
                ),
                (
                    "text",
                    models.ForeignKey(
                        blank=True,
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buttonurl_list",
                        to="data_handler.text",
                        verbose_name="Текст",
                    ),
                ),
            ],
            options={
                "verbose_name": "Кнопка на сайт",
                "verbose_name_plural": "Кнопки на сайт",
            },
        ),
        migrations.CreateModel(
            name="TextButtonSlug",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Порядок кнопки в меню"
                    ),
                ),
                (
                    "button",
                    models.ForeignKey(
                        blank=True,
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="textslug_list",
                        to="data_handler.buttonslug",
                        verbose_name="Кнопка",
                    ),
                ),
                (
                    "text",
                    models.ForeignKey(
                        blank=True,
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buttonslug_list",
                        to="data_handler.text",
                        verbose_name="Текст",
                    ),
                ),
            ],
            options={
                "verbose_name": "Кнопка на текст",
                "verbose_name_plural": "Кнопки на текст",
            },
        ),
        migrations.AddField(
            model_name="text",
            name="button_slug",
            field=models.ManyToManyField(
                related_name="button",
                through="data_handler.TextButtonSlug",
                to="data_handler.buttonslug",
            ),
        ),
        migrations.AddField(
            model_name="text",
            name="button_url",
            field=models.ManyToManyField(
                related_name="button",
                through="data_handler.TextButtonUrl",
                to="data_handler.buttonurl",
            ),
        ),
        migrations.AddField(
            model_name="telegarmuser",
            name="requests",
            field=models.ManyToManyField(
                related_name="requestuser",
                through="data_handler.UserRequest",
                to="data_handler.request",
            ),
        ),
        migrations.AddField(
            model_name="request",
            name="text",
            field=models.ForeignKey(
                blank=True,
                help_text="Выберите текст для ответа на запрос",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="request",
                to="data_handler.text",
                verbose_name="Текст",
            ),
        ),
        migrations.AddField(
            model_name="buttonslug",
            name="slug",
            field=models.ForeignKey(
                blank=True,
                help_text="Выберите слаг текста",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="data_handler.text",
                verbose_name="Слаг",
            ),
        ),
        migrations.AddConstraint(
            model_name="userrequest",
            constraint=models.UniqueConstraint(
                fields=("user", "request"), name="request_user_model"
            ),
        ),
        migrations.AddConstraint(
            model_name="textbuttonurl",
            constraint=models.UniqueConstraint(
                fields=("button", "text"), name="buttonurl_text_model"
            ),
        ),
        migrations.AddConstraint(
            model_name="textbuttonslug",
            constraint=models.UniqueConstraint(
                fields=("button", "text"), name="buttonslug_text_model"
            ),
        ),
        migrations.AddIndex(
            model_name="request",
            index=django.contrib.postgres.indexes.BrinIndex(
                fields=["created_at"], name="data_handle_created_a3ff26_brin"
            ),
        ),
        migrations.AddIndex(
            model_name="request",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["tsv"], name="data_handle_tsv_6f1e24_gin"
            ),
        ),
    ]