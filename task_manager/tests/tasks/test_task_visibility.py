from rest_framework import status
from rest_framework.test import APITestCase

from task_manager.models import ProjectMember
from task_manager.tests.factories.project import create_project
from task_manager.tests.factories.task import create_task
from task_manager.tests.helpers.api import auth_client
from task_manager.tests.helpers.auth import create_user
from task_manager.tests.helpers.project_membership import add_user_to_project


class TaskVisibilityTests(APITestCase):
    ROLES = (
        ProjectMember.Roles.OWNER,
        ProjectMember.Roles.MANAGER,
        ProjectMember.Roles.MEMBER,
    )

    def _prepare_visibility_case(self, role):
        user = create_user(f"user_{role}")
        stranger = create_user(f"stranger_{role}")

        project = create_project(owner=user)
        other_project = create_project(owner=stranger)

        add_user_to_project(project, user, role)

        task = create_task(
            project=project,
            created_by=user,
            title="Visible task",
        )
        foreign_task = create_task(
            project=other_project,
            created_by=stranger,
            title="Hidden task",
        )

        client = auth_client(user)

        return client, project, task, foreign_task

    def test_project_member_sees_only_tasks_from_his_project(self):
        for role in self.ROLES:
            client, project, task, foreign_task = self._prepare_visibility_case(role)

            response = client.get(f"/api/v1/projects/{project.id}/tasks/")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["id"], task.id)

    def test_project_member_cannot_retrieve_foreign_task(self):
        for role in self.ROLES:
            client, project, task, foreign_task = self._prepare_visibility_case(role)

            response = client.get(
                f"/api/v1/projects/{project.id}/tasks/{foreign_task.id}/"
            )

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
