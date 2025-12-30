from rest_framework.permissions import BasePermission
from task_manager.api.permissions.mixins import ProjectMemberMixin

from task_manager.models import ProjectMember


class TaskPermission(ProjectMemberMixin, BasePermission):
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