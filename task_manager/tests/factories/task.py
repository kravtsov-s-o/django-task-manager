from task_manager.models import Task


def create_task(**kwargs):
    return Task.objects.create(
        title=kwargs.get("title"),
        project=kwargs.get("project"),
        created_by=kwargs.get("created_by"),
        assignee=kwargs.get("assignee"),
    )