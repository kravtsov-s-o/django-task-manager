from task_manager.models import ProjectMember


def add_user_to_project(project, user, role):
    if ProjectMember.objects.filter(project=project, user=user).exists():
        return

    ProjectMember.objects.create(
        project=project,
        user=user,
        role=role,
    )
