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


class QuestionUpdateSerializer(serializers.ModelSerializer):
    question_id = serializers.UUIDField(required=False)

    class Meta:
        model = Questions
        fields = ['question_id', 'question', 'type', 'order', 'metadata']


class SurveyUpdateSerializer(serializers.ModelSerializer):
    questions = QuestionUpdateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Surveys
        fields = '__all__'
        read_only_fields = ['created_by', 'created_date']

    def update(self, instance, validated_data):
        question_list = validated_data.pop("questions", [])
        shared_with = validated_data.pop("shared_with", [])

        with transaction.atomic():
            # Update survey fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Update shared_with M2M
            instance.shared_with.set(shared_with)

            # Handle questions
            existing_questions = {q.question_id: q for q in instance.questions.all()}
            new_questions = []

            for question_data in question_list:
                q_id = question_data.get("question_id")
                if q_id and q_id in existing_questions:
                    # Update existing question
                    question_obj = existing_questions[q_id]
                    for attr, value in question_data.items():
                        if attr != "question_id":
                            setattr(question_obj, attr, value)
                    question_obj.save()
                else:
                    # New question to create
                    new_questions.append(Questions(survey=instance, **question_data))

            if new_questions:
                Questions.objects.bulk_create(new_questions)

            # Delete questions removed in the update
            updated_ids = [q.get("question_id") for q in question_list if q.get("question_id")]
            to_delete = instance.questions.exclude(question_id__in=updated_ids)
            to_delete.delete()

        return instance
