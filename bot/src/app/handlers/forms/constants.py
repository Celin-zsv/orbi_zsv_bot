# General constants

SHOW_FORM_FIELDS_TEXT = "Ваша анкета:\n" "Имя: {name}\n" "Email: {email}\n"

FORM_ACCEPTED_TEXT = "Ваша анкета принята, спасибо!"

FROM_CREATION_CANCELED_TEXT = "Создание анкеты успешно отменено." '\nДля создания новой нажмите "Указать данные".'

EMAIL_REGEXP = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

# Keyboards

ADD_DATA_BUTTON_TEXT = "Указать данные"
ANOTHER_FORM_BUTTON_TEXT = "Другой вариант"
BACK_BUTTON_TEXT = "<< Назад"
CANCEL_BUTTON_TEXT = "Отменить создание анкеты"
CANCEL_SENDING_BUTTON_TEXT = "Отменить"
DONATION_BUTTON_TEXT = "Сделать пожертвование"
RECREATE_FORM_BUTTON_TEXT = "Заполнить анкету заново"
SEND_FORM_BUTTON_TEXT = "Отправить"
FILL_BIRTHDAY_FORM_BUTTON_TEXT = "Провести день рождения в пользу фонда"
FILL_RUN_FORM_BUTTON_TEXT = "Пробежать за ОРБИ"

BACK_FORM_BUTTON_CALLBACK = "form_menu"
CANCEL_BUTTON_CALLBACK = "cancel"
DONATION_BUTTON_CALLBACK = "make_donation"
SEND_FORM_BUTTON_CALLBACK = "send_form"

ADD_FORM_DATA_CALLBACK = "add_form_data"

FILL_BIRTHDAY_FORM_CALLBACK = "birthday_form"

FILL_ANOTHER_FORM_CALLBACK = "another_help_form"

FILL_RUN_FORM_CALLBACK = "run_form"

# Another form

ANOTHER_FORM_START_TEXT = "Как бы Вы хотели помочь ОРБИ?\n" "Заполните все поля анкеты и мы свяжемся с вами"
ADD_HELP_TEXT = "Напишите, как Вы готовы помочь ОРБИ"
SHOW_ANOTHER_HELP_FORM_TEXT = SHOW_FORM_FIELDS_TEXT + "Предложение о помощи: {help}.\n"
HELP_TEXT_VALIDATION_ERROR = "Предложение о помощи не может состоять только из цифр.\n" "Введите корректное значение!"

# Birthday form

BIRTHDAY_FORM_START_TEXT = (
    "Проведите День рождения в пользу фонда ОРБИ! \n Заполните все "
    "поля анкеты и мы свяжемся с вами, чтобы рассказать подробности"
)
ADD_NAME_TEXT = "Укажите свое имя"
NAME_VALIDATION_ERROR_TEXT = "Имя не может состоять только из цифр." "\nВведите корректное значение!"
ADD_EMAIL_TEXT = "Теперь укажите свой email"
ADD_DATE_TEXT = "Теперь укажите дату в формате дд.мм.гггг"
EMAIL_VALIDATION_ERROR_TEXT = "Введено некорректное значение для email." "\nВведите корректное значение!"
DATE_VALIDATION_ERROR_TEXT = (
    "Дата указана в прошлом, либо указана в неправильном формате." "\nВведите корректное значение в формате дд.мм.гггг!"
)
SHOW_BIRTHDAY_FORM_FIELDS_TEXT = SHOW_FORM_FIELDS_TEXT + "Дата: {date}.\n"

# Run form

RUN_FORM_START_TEXT = (
    "Пробежка в пользу фонда ОРБИ!\nЗаполните все поля " "анкеты и мы свяжемся с вами, чтобы рассказать подробности."
)
