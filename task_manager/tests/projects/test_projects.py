from rest_framework import status
from rest_framework.test import APITestCase

from task_manager.models import Project, ProjectMember
from task_manager.tests.factories.project import create_project
from task_manager.tests.helpers.api import auth_client
from task_manager.tests.helpers.auth import create_user


class ProjectAPITest(APITestCase):
    def test_user_sees_only_own_projects(self):
        user1 = create_user("user1")
        user2 = create_user("user2")

        create_project(owner=user1, title="User1 project")
        create_project(owner=user2, title="User2 project")

        client = auth_client(user1)
        response = client.get("/api/v1/projects/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "User1 project")

    def test_user_can_create_project(self):
        user = create_user("user")
        client = auth_client(user)

        response = client.post(
            "/api/v1/projects/",
            {"title": "User new project"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(title="User new project").exists())

    def test_owned_added_to_project_members(self):
        user = create_user("user")
        client = auth_client(user)

        response = client.post(
            "/api/v1/projects/",
            {"title": "User new project"},
        )

        project_id = response.data["id"]

        membership_exists = ProjectMember.objects.filter(
            project_id=project_id,
            user=user,
            role=ProjectMember.Roles.OWNER,
        ).exists()

        self.assertTrue(membership_exists)

    def test_user_cannot_update_stranger_project(self):
        owner = create_user("owner")
        stranger = create_user("stranger")

        project = create_project(owner=owner)

        client = auth_client(stranger)
        response = client.patch(
            f"/api/v1/projects/{project.id}/",
            {"title": "Different title"},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_project(self):
        user = create_user("user")
        project = create_project(owner=user, title="Old title")

        client = auth_client(user)
        response = client.patch(
            f"/api/v1/projects/{project.id}/",
            {"title": "New title"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.title, "New title")

    def test_user_can_retrieve_own_project(self):
        user = create_user("user")
        project = create_project(owner=user)

        client = auth_client(user)
        response = client.get(f"/api/v1/projects/{project.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], project.id)


    def test_user_can_retrieve_stranger_project(self):
        owner = create_user("owner")
        stranger = create_user("stranger")
        project = create_project(owner=owner)

        client = auth_client(stranger)
        response = client.get(f"/api/v1/projects/{project.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
