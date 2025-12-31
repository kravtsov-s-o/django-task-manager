from task_manager.models import ProjectMember


def validate_project_membership(*, project_id, user):
    """
    Checks whether a user is a member of a project.

    Returns the ProjectMember instance if found,
    otherwise returns None.
    """

    try:
        return ProjectMember.objects.get(
            project_id=project_id,
            user=user,
        )
    except ProjectMember.DoesNotExist:
        return None
