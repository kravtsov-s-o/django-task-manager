from django.contrib.auth import get_user_model
from rest_framework import serializers

from task_manager.api.serializers.common import UserShortSerializer, ProjectShortSerializer
from task_manager.models import Task, ProjectMember

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks within a project.

    Handles assignee validation, restricts assignment
    to project members, and enforces role-based updates.
    """
    status = serializers.ChoiceField(
        choices=Task.Status.choices,
        write_only=True,
    )
    status_display = serializers.SerializerMethodField(read_only=True)

    def get_status_display(self, obj):
        return obj.get_status_display().lower()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        project_pk = self.context.get('project_pk')
        if project_pk:
            self.fields['assignee'].queryset = User.objects.filter(
                projectmember__project_id=project_pk
            ).exclude(
                projectmember__role=ProjectMember.Roles.OWNER
            )

    def validate_assignee(self, value):
        if value is None:
            return value

        project_pk = self.context.get('project_pk')
        if not project_pk:
            return value

        try:
            project_member = ProjectMember.objects.get(
                project=project_pk,
                user=value,
            )
        except ProjectMember.DoesNotExist:
            raise serializers.ValidationError(
                "Assignee must be a project member."
            )

        if project_member.role == ProjectMember.Roles.OWNER:
            raise serializers.ValidationError(
                "Project owner cannot be assigned to task."
            )

        return value

    assignee_data = UserShortSerializer(
        source="assignee",
        read_only=True,
    )

    created_by_data = UserShortSerializer(
        source="created_by",
        read_only=True,
    )

    project_data = ProjectShortSerializer(
        source="project",
        read_only=True,
    )

    class Meta:
        model = Task
        fields = (
            'id',
            'project',
            'project_data',
            'title',
            'description',
            'status',
            'status_display',
            'assignee',
            'assignee_data',
            'created_by',
            'created_by_data',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'project',
            'created_by',
            'created_at',
            'updated_at'
        )


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("status",)
