from rest_framework import generics

from accounts.models import User
from accounts.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
