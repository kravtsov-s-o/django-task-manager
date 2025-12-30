from rest_framework.permissions import SAFE_METHODS

from task_manager.api.permissions.utils import get_project_membership


class ProjectMemberMixin:
    """
    Provides helper to check project membership.
    """

    def get_membership(self, request, project):
        return get_project_membership(
            user=request.user,
            project=project,
        )

    def is_safe_method(self, request):
        return request.method in SAFE_METHODS