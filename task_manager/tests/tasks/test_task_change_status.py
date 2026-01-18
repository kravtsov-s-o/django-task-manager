import random

from rest_framework import status
from rest_framework.test import APITestCase

from task_manager.models import ProjectMember, Task
from task_manager.tests.factories.project import create_project
from task_manager.tests.factories.task import create_task
from task_manager.tests.helpers.api import auth_client
from task_manager.tests.helpers.auth import create_user
from task_manager.tests.helpers.project_membership import add_user_to_project


class TestTaskAPIChangeStatus(APITestCase):
    ROLES = (
        ProjectMember.Roles.OWNER,
        ProjectMember.Roles.MANAGER,
        ProjectMember.Roles.MEMBER,
    )

    def _prepare_change_status_case(self):
        owner = create_user(f"owner_{random.randint(0, 100)}")
        manager = create_user(f"manager_{random.randint(0, 100)}")
        member = create_user(f"member_{random.randint(0, 100)}")
        unassigned_member = create_user(f"unassigned_member_{random.randint(0, 100)}")

        project = create_project(owner=owner)

        add_user_to_project(project, manager, ProjectMember.Roles.MANAGER)
        add_user_to_project(project, member, ProjectMember.Roles.MEMBER)
        add_user_to_project(project, unassigned_member, ProjectMember.Roles.MEMBER)

        task = create_task(
            project=project,
            title=f"Task title",
            description=f"Task description",
            created_by=owner,
            assignee=member,
            status=Task.Status.TODO
        )

        return project, task, owner, manager, member, unassigned_member

    def test_owner_can_change_task_status(self):
        project, task, owner, *_ = self._prepare_change_status_case()

        client = auth_client(owner)

        response = client.patch(
            f"/api/v1/projects/{project.id}/tasks/{task.id}/change-status/",
            {
                'status': Task.Status.IN_PROGRESS
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Task.Status.IN_PROGRESS)

    def test_manager_can_change_task_status(self):
        project, task, _, manager, *_ = self._prepare_change_status_case()

        client = auth_client(manager)

        response = client.patch(
            f"/api/v1/projects/{project.id}/tasks/{task.id}/change-status/",
            {
                'status': Task.Status.IN_PROGRESS
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Task.Status.IN_PROGRESS)

    def test_assignee_member_can_change_task_status(self):
        project, task, _, _, member, *_ = self._prepare_change_status_case()

        client = auth_client(member)

        response = client.patch(
            f"/api/v1/projects/{project.id}/tasks/{task.id}/change-status/",
            {
                'status': Task.Status.IN_PROGRESS
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Task.Status.IN_PROGRESS)

    def test_unassigned_member_can_change_task_status(self):
        project, task, _, _, _, unassigned_member = self._prepare_change_status_case()

        client = auth_client(unassigned_member)

        response = client.patch(
            f"/api/v1/projects/{project.id}/tasks/{task.id}/change-status/",
            {
                'status': Task.Status.IN_PROGRESS
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
