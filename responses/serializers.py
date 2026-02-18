from rest_framework import serializers
from django.db import transaction
from .models import Responses, Answers
from users.serializers import UserSerializer
from surveys.models import Questions


class AnswerCreateSerializer(serializers.Serializer):
    answer = serializers.CharField(required=True)
    question = serializers.UUIDField()

    def validate_question(self, value):
        try:
            question = Questions.objects.get(question_id=value)
        except Questions.DoesNotExist:
            raise serializers.ValidationError("Invalid question ID")

        return question


class AnswerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ["answer", "question", "answer_id"]


class ResponseListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Responses
        fields = '__all__'


class ResponseCreateSerializer(serializers.ModelSerializer):
    answers = AnswerCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Responses
        fields = '__all__'
        read_only_fields = ['created_by', 'survey']

    def validate(self, data):
        answers = data.get("answers", [])
        if not answers:
            raise serializers.ValidationError(
                "You must answer atleast one question.")
        return data

    def create(self, validated_data):
        answer_list = validated_data.pop("answers", [])
        survey = self.context.get("survey")
        user = self.context.get("user")

        with transaction.atomic():
            response = Responses.objects.create(
                created_by=user, survey=survey, **validated_data)
            answer_objects = [
                Answers(response=response, **each_answer) for each_answer in answer_list]
            Answers.objects.bulk_create(answer_objects)
        return response


class ResponseReadSerializer(serializers.ModelSerializer):
    answers = AnswerReadSerializer(source="answers_response", many=True)
    created_by = UserSerializer()

    class Meta:
        model = Responses
        fields = ["response_id", "created_by",
                  "created_date", "survey", "answers"]
