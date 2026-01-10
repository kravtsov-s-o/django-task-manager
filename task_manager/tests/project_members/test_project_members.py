from rest_framework import status
from rest_framework.test import APITestCase

from task_manager.models import ProjectMember
from task_manager.tests.factories.project import create_project
from task_manager.tests.helpers.api import auth_client
from task_manager.tests.helpers.auth import create_user
from task_manager.tests.helpers.project_membership import add_user_to_project


class ProjectMemberAPITests(APITestCase):
    def test_owner_can_add_project_member(self):
        owner = create_user("owner")
        new_user = create_user("member")

        project = create_project(owner=owner)
        client = auth_client(owner)

        response = client.post(
            f"/api/v1/projects/{project.id}/members/",
            {
                "user": new_user.id,
                "role": ProjectMember.Roles.MEMBER,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            ProjectMember.objects.filter(
                project=project,
                user=new_user,
                role=ProjectMember.Roles.MEMBER,
            ).exists()
        )

    def test_manager_can_add_member(self):
        owner = create_user("owner")
        manager = create_user("manager")
        member = create_user("member")

        project = create_project(owner=owner)

        add_user_to_project(project, manager, ProjectMember.Roles.MANAGER)

        client = auth_client(manager)
        response = client.post(
            f"/api/v1/projects/{project.id}/members/",
            {
                "user": member.id,
                "role": ProjectMember.Roles.MEMBER,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_cannot_add_manager_or_owner(self):
        owner = create_user("owner")
        manager = create_user("manager")
        new_manager = create_user("new_manager")

        project = create_project(owner=owner)

        add_user_to_project(project, manager, ProjectMember.Roles.MANAGER)

        client = auth_client(manager)
        response = client.post(
            f"/api/v1/projects/{project.id}/members/",
            {
                "user": new_manager.id,
                "role": ProjectMember.Roles.MANAGER,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_member_cannot_add_project_member(self):
        owner = create_user("owner")
        member = create_user("member")
        stranger = create_user("stranger")

        project = create_project(owner=owner)

        add_user_to_project(project, member, ProjectMember.Roles.MEMBER)

        client = auth_client(member)
        response = client.post(
            f"/api/v1/projects/{project.id}/members/",
            {
                "user": stranger.id,
                "role": ProjectMember.Roles.MEMBER,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_add_duplicate_project_member(self):
        owner = create_user("owner")
        member = create_user("member")

        project = create_project(owner=owner)

        add_user_to_project(project, member, ProjectMember.Roles.MEMBER)

        client = auth_client(member)
        response = client.post(
            f"/api/v1/projects/{project.id}/members/",
            {
                "user": member.id,
                "role": ProjectMember.Roles.MEMBER,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_cannot_be_removed(self):
        owner = create_user("owner")
        project = create_project(owner=owner)

        owner_membership = ProjectMember.objects.get(
            project=project,
            user=owner,
        )

        client = auth_client(owner)
        response = client.delete(
            f"/api/v1/projects/{project.id}/members/{owner_membership.id}/",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)