from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProjectPermission(BasePermission):
    """
    Permission rules for project-level operations.

    Only the project owner is allowed to modify or delete a project.
    All authenticated users may read project data.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user
