from django.contrib.auth import get_user_model
from rest_framework import serializers

from task_manager.api.serializers.common import UserShortSerializer, ProjectShortSerializer
from task_manager.models import ProjectMember

User = get_user_model()


class ProjectMemberSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        project_pk = self.context.get('project_pk')
        if project_pk:
            self.fields['user'].queryset = User.objects.exclude(
                projectmember__project_id=project_pk,
                projectmember__role=ProjectMember.Roles.OWNER
            )

    role = serializers.ChoiceField(
        choices=[
            (role.value, role.label)
            for role in ProjectMember.Roles
            if role != ProjectMember.Roles.OWNER
        ],
        write_only=True,
    )
    role_display = serializers.SerializerMethodField(read_only=True)

    def get_role_display(self, obj):
        return obj.get_role_display().lower()

    user_data = UserShortSerializer(
        source="user",
        read_only=True,
    )

    project_data = ProjectShortSerializer(
        source="project",
        read_only=True,
    )

    def validate_role(self, value):
        if value == ProjectMember.Roles.OWNER:
            raise serializers.ValidationError("Owner role cannot be assigned.")
        return value

    def validate(self, attrs):
        project_pk = self.context.get("project_pk")
        user = attrs.get("user")

        if ProjectMember.objects.filter(
                project_id=project_pk,
                user=user,
        ).exists():
            raise serializers.ValidationError(
                "User is already a project member."
            )

        return attrs

    class Meta:
        model = ProjectMember
        fields = (
            "id",
            "project",
            "project_data",
            "user",
            "user_data",
            "role",
            "role_display",
            "joined_at"
        )
        read_only_fields = (
            "id",
            "project",
            "joined_at"
        )
