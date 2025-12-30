from task_manager.models import ProjectMember


def validate_project_membership(*, project_id, user):
    try:
        return ProjectMember.objects.get(
            project_id=project_id,
            user=user,
        )
    except ProjectMember.DoesNotExist:
        return None
