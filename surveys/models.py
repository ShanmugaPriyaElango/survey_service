import uuid
from django.db import models

from users.models import Users


class Surveys(models.Model):
    survey_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(
        Users, related_name='surveys_created', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(
        Users, related_name='shared_surveys', blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Questions(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('text', 'Text'),
        ('rank', 'Rank'),
        ('bool', 'True/False'),
    ]
    question_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=300)
    type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    order = models.PositiveIntegerField(default=0)
    survey = models.ForeignKey(
        Surveys, related_name='questions', on_delete=models.CASCADE)
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.question
