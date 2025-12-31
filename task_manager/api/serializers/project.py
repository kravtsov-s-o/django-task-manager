from rest_framework import serializers
from task_manager.api.serializers.common import UserShortSerializer
from task_manager.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for project entities.

    Used to create, retrieve and update project data.
    Exposes owner information in a read-only format.
    """

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'owner',
            'owner_data',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )

    owner_data = UserShortSerializer(
        source="owner",
        read_only=True,
    )
