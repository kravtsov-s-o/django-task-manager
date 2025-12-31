from task_manager.models import ProjectMember


def get_project_membership(*, user, project):
    """
    Retrieves project membership for a given user.

    Returns a ProjectMember instance if the user belongs
    to the project, otherwise returns None.
    """
    try:
        return ProjectMember.objects.get(
            user=user,
            project=project,
        )
    except ProjectMember.DoesNotExist:
        return None
