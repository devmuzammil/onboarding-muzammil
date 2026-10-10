
from django.db.models import Count, Q
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer
from .permissions import IsOwner

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "priority"]
    search_fields = ["title"]
    ordering_fields = ["due_date"]
    ordering = ["due_date"]

    def get_queryset(self):
        queryset = (
            Task.objects
            .select_related("project", "owner")
            .prefetch_related("tags")
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.status = Task.Status.COMPLETED
        task.save(update_fields=["completed", "status"])

        return Response(
            {
                "message": "Task marked as completed.",
                "id": task.id,
                "completed": task.completed,
                "status": task.status,
            },
            status=status.HTTP_200_OK,
        )
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        project = self.get_object()

        counts = project.tasks.aggregate(
            total=Count("id"),
            completed=Count("id", filter=Q(completed=True)),
            incomplete=Count("id", filter=Q(completed=False)),
        )

        return Response({
            "project_id": project.id,
            "project_name": project.name,
            "tasks": counts,
        })