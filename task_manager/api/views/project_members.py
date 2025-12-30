from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from task_manager.api.permissions.project_member import ProjectMemberPermission
from task_manager.api.serializers.project_member import ProjectMemberSerializer

from task_manager.models import Project, ProjectMember, Task

class ProjectMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated, ProjectMemberPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_pk"] = self.kwargs.get("project_pk")
        return context

    def get_queryset(self):
        return ProjectMember.objects.filter(
            project_id=self.kwargs["project_pk"]
        )

    def perform_create(self, serializer):
        project = get_object_or_404(
            Project,
            pk=self.kwargs["project_pk"],
            projectmember__user=self.request.user,
        )

        serializer.save(
            project=project,
        )