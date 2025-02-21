from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    серіалізатор перетворює екземпляри моделі User у JSON та назад.
    Він включає такі поля: id, username, email, first_name, last_name та password.
    Поле password є лише для запису і вимагає мінімальну довжину 8 символів.

    Методи:
        create(validated_data):
            Створює та повертає новий екземпляр User з урахуванням перевірених даних.

    Атрибути:
        Meta:
             model: Модель, пов'язана з цим серіалізатором, отримана за допомогою get_user_model().
             fields: Поля, що включаються до серіалізованого виводу.
             read_only_fields: Поля, що є лише для читання (id).
             extra_kwargs: Додаткові налаштування для певних полів (password).
    """

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
        )
        read_only_field = ("id")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8
            },
        }


        def create (self, validated_data):
            """
            Створює та повертає новий екземпляр User.

            З використанням перевірених даних, цей метод створює новий екземпляр
            User за допомогою методу create_user моделі User.

            Аргументи:
                validated_data (dict): Перевірені дані, що містять атрибути користувача.

            Повертає:
                Новий екземпляр User.
            """
            return get_user_model().object.create_useer(**validated_data)
