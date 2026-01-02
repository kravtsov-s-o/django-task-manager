from rest_framework import generics
from rest_framework.permissions import AllowAny

from api.auth.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
