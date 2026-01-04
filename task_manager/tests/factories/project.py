from task_manager.models import Project, ProjectMember


def create_project(owner, title="Test Project"):
    project = Project.objects.create(
        owner=owner,
        title=title
    )
    ProjectMember.objects.create(
        project=project,
        user=owner,
        role=ProjectMember.Roles.OWNER
    )
    return project
