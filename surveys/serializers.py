from rest_framework import serializers
from .models import Surveys, Questions
from users.serializers import UserSerializer
from django.db import transaction


class QuestionCreateSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=300)
    type = serializers.CharField(max_length=10)
    order = serializers.IntegerField()
    metadata = serializers.JSONField(default=dict)


class QuestionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ["question_id", "question", "type", "order", "metadata"]


class SurveyListSerializer(serializers.ModelSerializer):
    shared_with = UserSerializer(many=True)
    created_by = UserSerializer()

    class Meta:
        model = Surveys
        fields = '__all__'


class SurveyCreateSerializer(serializers.ModelSerializer):
    questions = QuestionCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Surveys
        fields = '__all__'
        read_only_fields = ['created_by', 'created_date']

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        question_list = validated_data.pop("questions", [])
        shared_with = validated_data.pop("shared_with", [])
        with transaction.atomic():
            survey = Surveys.objects.create(
                created_by=user, **validated_data)
            survey.shared_with.set(shared_with)
            question_objects = [Questions(
                survey=survey, **each_question) for each_question in question_list]
            Questions.objects.bulk_create(question_objects)
        return survey


class SurveyReadSerializer(serializers.ModelSerializer):
    questions = QuestionReadSerializer(many=True)
    shared_with = UserSerializer(many=True)
    created_by = UserSerializer()

    class Meta:
        model = Surveys
        fields = ["survey_id", "name", "description",
                  "shared_with", "created_by", "created_date", "questions", "is_published"]
        read_only_fields = ["created_by"]
