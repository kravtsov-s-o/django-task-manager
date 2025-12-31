from rest_framework.permissions import SAFE_METHODS

from task_manager.api.permissions.utils import get_project_membership


class ProjectMemberMixin:
    """
    Shared helper methods for project-based permission checks.

    Provides utilities to determine whether the current user
    is a member of a given project and to identify safe requests.
    """

    def get_membership(self, request, project):
        return get_project_membership(
            user=request.user,
            project=project,
        )

    def is_safe_method(self, request):
        return request.method in SAFE_METHODS
