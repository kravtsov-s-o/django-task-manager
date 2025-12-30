from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from task_manager.api.permissions.project import ProjectPermission
from task_manager.api.serializers.project import ProjectSerializer

from task_manager.models import Project, ProjectMember, Task

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def get_queryset(self):
        return Project.objects.filter(projectmember__user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)

        ProjectMember.objects.create(
            project=project,
            user=self.request.user,
            role=ProjectMember.Roles.OWNER,
        )