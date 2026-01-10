from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from task_manager.models import ProjectMember, Task
from task_manager.tests.factories.project import create_project
from task_manager.tests.helpers.api import auth_client
from task_manager.tests.helpers.auth import create_user
from task_manager.tests.helpers.project_membership import add_user_to_project


class TaskCreateAPITests(APITestCase):
    FORBIDDEN_ROLES = (
        ProjectMember.Roles.MEMBER,
    )

    ALLOWED_ROLES = (
        ProjectMember.Roles.OWNER,
        ProjectMember.Roles.MANAGER,
    )

    def _prepare_create_case(self, role):
        owner = create_user(f"owner_{role}")
        project = create_project(owner=owner)

        if role == ProjectMember.Roles.OWNER:
            user = owner
        else:
            user = create_user(f"user_{role}")
            add_user_to_project(project, user, role)

        client = auth_client(user)

        return client, project, user

    def test_allowed_roles_can_create_tasks(self):
        for role in self.ALLOWED_ROLES:
            client, project, user = self._prepare_create_case(role)

            response = client.post(
                f"/api/v1/projects/{project.id}/tasks/",
                {
                    "title": "Test Task",
                    "description": "Test description",
                    "status": Task.Status.TODO,
                }
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["created_by"], user.id)

    def test_forbidden_roles_cannot_create_tasks(self):
        for role in self.FORBIDDEN_ROLES:
            client, project, user = self._prepare_create_case(role)

            response = client.post(
                f"/api/v1/projects/{project.id}/tasks/",
                {
                    "title": "Test Task",
                    "status": Task.Status.TODO,
                }
            )

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_create_task_in_foreign_project(self):
        owner = create_user("owner")
        stranger = create_user("stranger")

        project = create_project(owner=owner)

        client = auth_client(stranger)
        response = client.post(
            f"/api/v1/projects/{project.id}/tasks/",
            {
                "title": "Hack Task",
                "status": Task.Status.TODO,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
