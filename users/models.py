import uuid
from django.db import models


class Users(models.Model):
    USER_ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('answerer', 'Answerer'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(blank=False, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)

    def __str__(self):
        return self.name


class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)


class RolePermission(models.Model):
    role = models.CharField(max_length=20)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
