from task_manager.models import ProjectMember


def get_project_membership(*, user, project):
    try:
        return ProjectMember.objects.get(
            user=user,
            project=project,
        )
    except ProjectMember.DoesNotExist:
        return None