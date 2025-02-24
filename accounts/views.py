from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts.models import User
from accounts.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
