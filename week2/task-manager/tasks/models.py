from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)

class Task(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    completed=models.BooleanField(default=False)
    due_date=models.DateTimeField()
    project=models.ForeignKey(Project,on_delete=models.CASCADE)