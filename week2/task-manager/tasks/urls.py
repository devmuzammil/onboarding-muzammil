from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet,ProjectViewSet

router=DefaultRouter()
router.register("api/v1/tasks",TaskViewSet,basename="task")
router.register("api/v1/projects",ProjectViewSet,basename="project")

urlpatterns=[
    path("",include(router.urls))
]
