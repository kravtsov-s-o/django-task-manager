from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, related_name='projects', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class ProjectMember(models.Model):
    class Roles(models.IntegerChoices):
        OWNER = 1
        MANAGER = 2
        MEMBER = 3

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=Roles.choices, default=Roles.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['project', '-joined_at']
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_user_project',
            )
        ]


class Task(models.Model):
    class Status(models.IntegerChoices):
        TODO = 1
        IN_PROGRESS = 2
        DONE = 3

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.TODO)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
