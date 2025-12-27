from django.contrib import admin
from .models import Project, ProjectMember, Task


# Register your models here.
class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    can_delete = False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectMemberInline]
    list_display = ('title', 'owner', 'created_at', 'updated_at')
    search_fields = ('title',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assignee', 'created_by', 'created_at', 'updated_at')
    list_filter = ('status', 'assignee', 'created_by')
    search_fields = ('title',)
