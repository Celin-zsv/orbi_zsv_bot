from django.contrib.auth.models import AbstractUser
from django.db import models
from expert_system.settings import ADMIN, USER

CHOICES = (
    (USER, "Пользователь"),
    (ADMIN, "Администратор"),
)
NAMING_LENGTH = 150


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=NAMING_LENGTH,
        unique=True,
        verbose_name="Логин",
        help_text="Введите логин",
    )
    email = models.EmailField(
        max_length=256,
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите электронную почту",
    )
    first_name = models.CharField(
        max_length=NAMING_LENGTH,
        unique=False,
        verbose_name="Имя",
        help_text="Введите имя",
    )
    last_name = models.CharField(
        max_length=NAMING_LENGTH,
        unique=False,
        verbose_name="Фамилия",
        help_text="Введите фамилию",
    )
    role = models.CharField(
        choices=CHOICES,
        max_length=42,
        default=CHOICES[0][0],
        verbose_name="Роль",
        help_text="Укажите роль",
    )
    confirmation_code = models.CharField(max_length=32, blank=True)

    @property
    def is_admin(self):
        return (self.role == ADMIN or self.is_staff) and self.is_authenticated

    def __str__(self):
        return self.username

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
