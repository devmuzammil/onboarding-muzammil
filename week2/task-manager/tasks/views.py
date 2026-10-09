from django.db.models import Count, Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer

class TaskViewSet(ModelViewSet):
    queryset = (
        Task.objects
        .select_related("project")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer
    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.save(update_fields=["completed"])
        return Response(
            {
                "message": "Task marked as completed.",
                "id": task.id,
                "completed": task.completed,
            },
            status=status.HTTP_200_OK,
        )
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        project = self.get_object()

        counts = project.tasks.aggregate(
            total=Count("id"),
            completed=Count(
                "id",
                filter=Q(completed=True),
            ),
            incomplete=Count(
                "id",
                filter=Q(completed=False),
            ),
        )
        return Response({
            "project_id": project.id,
            "project_name": project.name,
            "tasks": counts,
        })
