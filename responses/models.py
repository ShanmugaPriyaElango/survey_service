import uuid
from django.db import models
from surveys.models import Surveys, Questions
from users.models import Users


class Responses(models.Model):
    response_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(
        Surveys, related_name='responses', on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        Users, related_name='responses_created', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class Answers(models.Model):
    answer_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    answer = models.TextField(blank=False)
    response = models.ForeignKey(
        Responses, related_name='answers_response', on_delete=models.CASCADE)
    question = models.ForeignKey(
        Questions, related_name='answers_question', on_delete=models.CASCADE)
