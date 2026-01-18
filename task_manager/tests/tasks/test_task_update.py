from rest_framework import status
from rest_framework.test import APITestCase

from task_manager.models import ProjectMember, Task
from task_manager.tests.factories.project import create_project
from task_manager.tests.factories.task import create_task
from task_manager.tests.helpers.api import auth_client
from task_manager.tests.helpers.auth import create_user
from task_manager.tests.helpers.project_membership import add_user_to_project


class TaskUpdateAPITests(APITestCase):
    FORBIDDEN_ROLES = (
        ProjectMember.Roles.MEMBER,
    )

    ALLOWED_ROLES = (
        ProjectMember.Roles.OWNER,
        ProjectMember.Roles.MANAGER,
    )

    def _prepare_update_case(self, role):
        owner = create_user(f"owner_{role}")
        project = create_project(owner=owner)
        task = create_task(
            title="Test Task",
            created_by=owner,
            project=project,
            status=Task.Status.TODO
        )

        if role == ProjectMember.Roles.OWNER:
            user = owner
        else:
            user = create_user(f"user_{role}")
            add_user_to_project(project, user, role)

        client = auth_client(user)

        return client, project, user, task

    def test_allowed_roles_can_put_tasks(self):
        for role in self.ALLOWED_ROLES:
            client, project, user, task = self._prepare_update_case(role)

            response = client.put(
                f"/api/v1/projects/{project.id}/tasks/{task.id}/",
                {
                    "title": "New Title Task",
                    "description": "New description task",
                    "created_by": task.created_by,
                    "status": task.status,
                }
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["title"], "New Title Task")

    def test_allowed_roles_can_patch_tasks(self):
        for role in self.ALLOWED_ROLES:
            client, project, user, task = self._prepare_update_case(role)

            response = client.patch(
                f"/api/v1/projects/{project.id}/tasks/{task.id}/",
                {
                    "description": "New description task",
                }
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["description"], "New description task")

    def test_forbidden_roles_cannot_put_tasks(self):
        for role in self.FORBIDDEN_ROLES:
            client, project, user, task = self._prepare_update_case(role)

            response = client.put(
                f"/api/v1/projects/{project.id}/tasks/{task.id}/",
                {
                    "title": "New Title Task",
                    "description": "New description task",
                    "created_by": task.created_by,
                    "status": task.status,
                }
            )

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_roles_cannot_patch_tasks(self):
        for role in self.FORBIDDEN_ROLES:
            client, project, user, task = self._prepare_update_case(role)

            response = client.patch(
                f"/api/v1/projects/{project.id}/tasks/{task.id}/",
                {
                    "description": "New description task",
                }
            )

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
