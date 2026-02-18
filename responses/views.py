from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from .models import Responses, Answers
from surveys.models import Surveys
from surveyapp.permissions import IsAnswerer, IsAdmin
from .serializers import ResponseListSerializer, ResponseCreateSerializer, ResponseReadSerializer


class ResponseListCreateView(generics.ListCreateAPIView):
    queryset = Responses.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAnswerer()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ResponseCreateSerializer
        return ResponseListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["survey"] = self.get_survey()
        context["user"] = self.request.user

        return context

    def get_survey(self):
        return get_object_or_404(Surveys, survey_id=self.kwargs["survey_id"])

    def get_queryset(self):
        user = self.request.user
        survey_id = self.kwargs.get("survey_id")

        return self.queryset.filter(
            survey_id=survey_id).filter(Q(survey__created_by=user) |
                                        Q(survey__shared_with=user)
                                        ).select_related("created_by", "survey").prefetch_related("answers_response").distinct()

    def list(self, request, *args, **kwargs):
        user = self.request.user
        survey = self.get_survey()
        view_type = self.request.query_params.get("view", "").lower()
        if not (survey.created_by == user or user in survey.shared_with.all()):
            return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        if view_type == "aggregate":
            return self.get_aggregate_response(survey)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_aggregate_response(self, survey):
        answer_objects = (
            Answers.objects.filter(response__survey=survey)
            .values("question__question", "answer")
            .annotate(count=Count("answer"))
            .order_by("question__question")
        )
        result = {}
        for item in answer_objects:
            question = item["question__question"]
            if question not in result:
                result[question] = []
            result[question].append({
                "answer": item["answer"],
                "count": item["count"]
            })
        return Response(result, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        survey = self.get_survey()
        user = self.request.user
        if survey.is_published:
            previous_response = Responses.objects.filter(
                survey=survey, created_by=user)
            if previous_response.exists():
                raise ValidationError(
                    "You have already submitted response for this survey.")
            serializer.save()
        else:
            raise ValidationError("This survey is not available.")


class ResponseReadView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = ResponseReadSerializer
    queryset = Responses.objects.all()

    def get_queryset(self):
        user = self.request.user
        survey_id = self.kwargs.get("survey_id")
        if user.role == "admin":
            return self.queryset.filter(
                survey_id=survey_id).filter(Q(survey__created_by=user) |
                                            Q(survey__shared_with=user)
                                            ).select_related("created_by", "survey").prefetch_related("answers_response").distinct()
        return self.queryset.filter(survey_id=survey_id, created_by=user).select_related(
            "created_by", "survey").prefetch_related("answers_response")


class UserResponsesListView(generics.ListAPIView):
    serializer_class = ResponseListSerializer
    permission_classes = []

    def get_queryset(self):
        user = self.request.user
        user_id_params = self.request.query_params.get("user_id")

        if user.role == "admin":
            return Responses.objects.filter(
                created_by=user_id_params).filter(Q(survey__created_by=user) |
                                                  Q(survey__shared_with=user)).select_related("created_by", "survey").prefetch_related("answers_response").distinct()

        return Responses.objects.filter(created_by=user)
