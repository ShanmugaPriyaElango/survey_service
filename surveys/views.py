from rest_framework import generics
from django.db.models import Q

from .models import Surveys
from surveyapp.permissions import IsAdmin
from .serializers import SurveyListSerializer, SurveyCreateSerializer, SurveyReadSerializer


class SurveyListCreateView(generics.ListCreateAPIView):
    queryset = Surveys.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return []

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SurveyCreateSerializer
        return SurveyListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            queryset = self.queryset.filter(
                Q(created_by=user) | Q(shared_with=user)).prefetch_related("shared_with", "created_by").distinct()
        else:
            queryset = self.queryset.filter(
                is_published=True).prefetch_related("shared_with", "created_by")
        return queryset


class SurveyReadUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = []
    serializer_class = SurveyReadSerializer
    queryset = Surveys.objects.all()

    def get_permissions(self):
        if self.request.method == "PUT":
            return [IsAdmin()]
        return []

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            queryset = self.queryset.filter(
                Q(created_by=user) | Q(shared_with=user)).prefetch_related("shared_with", "created_by").distinct()
        else:
            queryset = self.queryset.filter(
                is_published=True).prefetch_related("shared_with", "created_by")

        return queryset
