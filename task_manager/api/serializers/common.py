from django.contrib.auth import get_user_model
from rest_framework import serializers

from task_manager.models import Project

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class ProjectShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "title")
