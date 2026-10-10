from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import TaskViewSet,ProjectViewSet

router=DefaultRouter()
router.register("api/v1/tasks",TaskViewSet,basename="task")
router.register("api/v1/projects",ProjectViewSet,basename="project")

urlpatterns=[
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path("",include(router.urls))
]
