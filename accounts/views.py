from rest_framework import generics

from accounts.models import User
from accounts.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """

    представлення дозволяє клієнтам створювати нових користувачів, надсилаючи POST-запит
    з необхідними даними користувача. Воно використовує `UserSerializer` для перевірки та
    серіалізації вхідних даних і створення нового екземпляра користувача в базі даних.

    Атрибути:
    queryset (QuerySet): Набір даних усіх об'єктів користувачів.
    serializer_class (Serializer): Клас серіалізатора, який використовується для перевірки та серіалізації даних.

    Методи:
    post(request, *args, **kwargs):
    Обробляє POST-запити для створення нового користувача.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
