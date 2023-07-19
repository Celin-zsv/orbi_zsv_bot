# Generated by Django 4.2.3 on 2023-07-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_handler", "request_field_tsvector_field_trigger"),
    ]

    operations = [
        migrations.AddField(
            model_name="text",
            name="is_published",
            field=models.BooleanField(
                default=True,
                help_text="Текст опубликован /снят с публикации",
                verbose_name="Опубликован",
            ),
        ),
    ]
