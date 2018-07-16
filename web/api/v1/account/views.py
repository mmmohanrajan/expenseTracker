from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import UserSerializer
from api.models import User
from api.permissions import IsAdminOrOwner, IsAdmin


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()


class UserRegister(generics.CreateAPIView):
    """
    Register a new user.
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    