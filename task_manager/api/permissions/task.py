from rest_framework.permissions import BasePermission, SAFE_METHODS
from task_manager.api.permissions.mixins import ProjectMemberMixin
from task_manager.api.permissions.utils import get_project_membership

from task_manager.models import ProjectMember


class TaskPermission(ProjectMemberMixin, BasePermission):
    """
    Permission rules for task operations within a project.

    Owner and Manager can fully manage tasks.
    Member can update task status only for tasks assigned to them.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        project_pk = view.kwargs.get("project_pk")
        if not project_pk:
            return False

        membership = ProjectMember.objects.filter(
            user=request.user,
            project=project_pk,
        ).first()

        if not membership:
            return True

        if membership.role == ProjectMember.Roles.MEMBER and request.method == "PATCH":
            return True

        return membership.role in (
            ProjectMember.Roles.OWNER,
            ProjectMember.Roles.MANAGER,
        )

        return True

    def has_object_permission(self, request, view, obj):
        if self.is_safe_method(request):
            return True

        membership = self.get_membership(request, obj.project)
        if not membership:
            return False

        if membership.role in (
                ProjectMember.Roles.OWNER,
                ProjectMember.Roles.MANAGER,
        ):
            return True

        if (
                membership.role == ProjectMember.Roles.MEMBER
                and request.method == "PATCH"
                and obj.assignee == request.user
        ):
            return True

        return False
