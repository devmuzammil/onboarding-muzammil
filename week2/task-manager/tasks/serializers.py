from rest_framework import serializers
from django.utils import timezone
from .models import Task, Project, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(
        source="project.name",
        read_only=True,
    )
    tag_names = serializers.StringRelatedField(
        source="tags",
        many=True,
        read_only=True,
    )
    class Meta:
        model = Task
        fields = ["id","title","description","completed","due_date","project","project_name","tags","tag_names",]

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Due Date can't be in the past."
            )
        return value

    def validate(self, data):
        title = data.get(
            "title",
            self.instance.title if self.instance else None,
        )

        project = data.get(
            "project",
            self.instance.project if self.instance else None,
        )

        existing_task = Task.objects.filter(
            title=title,
            project=project,
        )

        if self.instance:
            existing_task = existing_task.exclude(
                pk=self.instance.pk
            )

        if existing_task.exists():
            raise serializers.ValidationError({
                "title": "This title already exists in this project."
            })

        return data


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name"]