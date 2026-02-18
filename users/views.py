from django.shortcuts import render
from rest_framework import generics
from .models import Users
from .serializers import UserSerializer


class UsersListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer
    queryset = Users.objects.all()
