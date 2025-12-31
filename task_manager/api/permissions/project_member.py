from rest_framework.permissions import BasePermission
from task_manager.api.permissions.mixins import ProjectMemberMixin

from task_manager.api.permissions.utils import get_project_membership

from task_manager.models import ProjectMember


class ProjectMemberPermission(ProjectMemberMixin, BasePermission):
    """
    Permission rules for managing project members.

    Owner can manage all members except themselves.
    Manager can manage members only.
    Members have read-only access.
    """

    def has_permission(self, request, view):
        if self.is_safe_method(request):
            return True

        project_pk = view.kwargs.get("project_pk")
        if not project_pk:
            return False

        membership = get_project_membership(
            user=request.user,
            project=project_pk,
        )
        if not membership:
            return False

        return membership.role in (
            ProjectMember.Roles.OWNER,
            ProjectMember.Roles.MANAGER,
        )

    def has_object_permission(self, request, view, obj):
        if self.is_safe_method(request):
            return True

        membership = self.get_membership(request, obj.project)
        if not membership:
            return False

        if obj.role == ProjectMember.Roles.OWNER:
            return False

        if membership.role == ProjectMember.Roles.OWNER:
            return True

        if membership.role == ProjectMember.Roles.MANAGER:
            return obj.role == ProjectMember.Roles.MEMBER

        return False
