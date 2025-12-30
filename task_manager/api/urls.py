from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from task_manager.api.views.project import ProjectViewSet
from task_manager.api.views.project_members import ProjectMemberViewSet
from task_manager.api.views.task import TaskViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

projects_router = NestedDefaultRouter(
    router,
    r'projects',
    lookup='project'
)

projects_router.register(
    r'tasks',
    TaskViewSet,
    basename='project-tasks'
)

projects_router.register(
    r'members',
    ProjectMemberViewSet,
    basename='project-members'
)

urlpatterns = router.urls + projects_router.urls
