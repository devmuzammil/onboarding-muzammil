from django.urls import path
from .views import(
    TaskListCreateView,
    TaskRetrieveUpdateDestroyListView,
    ProjectListView,
    ProjectRetrieveUpdateDestroyListView
)


urlpatterns=[
    path("api/v1/tasks/",TaskListCreateView.as_view(),name="task-list"),
    path("api/v1/tasks/<int:pk>/",TaskRetrieveUpdateDestroyListView.as_view(),name="task-detail"),
    path("api/v1/projects/",ProjectListView.as_view(),name="project-list"),
    path("api/v1/projects/<int:pk>/",ProjectRetrieveUpdateDestroyListView.as_view(),name="project-details"),
]
