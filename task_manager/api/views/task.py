from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task_manager.api.permissions.task import TaskPermission
from task_manager.api.serializers.task import TaskSerializer, TaskStatusSerializer

from task_manager.models import Project, Task


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tasks within a project.

    Tasks are scoped to a single project and accessible
    only to users who are members of that project.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_pk"] = self.kwargs.get("project_pk")
        return context

    def get_queryset(self):
        return Task.objects.filter(
            project_id=self.kwargs["project_pk"],
            project__projectmember__user=self.request.user
        )

    def perform_create(self, serializer):
        project = get_object_or_404(
            Project,
            pk=self.kwargs["project_pk"],
            projectmember__user=self.request.user,
        )

        serializer.save(
            project=project,
            created_by=self.request.user,
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="change-status",
    )
    def change_status(self, request, project_pk=None, pk=None):
        task = self.get_object()

        serializer = TaskStatusSerializer(
            task,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
