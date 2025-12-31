from django.contrib.auth import get_user_model

from task_manager.models import ProjectMember

User = get_user_model()


class ProjectContextMixin:
    """
    Provides access to project identifier from serializer context.

    Intended for serializers that operate within a project scope
    and require project-specific validation or queryset restriction.
    """

    @property
    def project_pk(self):
        return self.context.get("project_pk")


class AssigneeQuerysetMixin(ProjectContextMixin):
    """
    Restricts assignee queryset to users who are members of the project.

    Project owners are excluded from assignment.
    """

    def restrict_assignee_queryset(self):
        if not self.project_pk:
            return

        self.fields["assignee"].queryset = (
            User.objects.filter(
                projectmember__project_id=self.project_pk
            )
            .exclude(
                projectmember__role=ProjectMember.Roles.OWNER
            )
        )
