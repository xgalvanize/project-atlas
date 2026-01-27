from django.db import models

# Create your models here.
from projects.models import Project

class Task(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="tasks",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        PENDING = "PENDING"
        IN_PROGRESS = "IN_PROGRESS"
        DONE = "DONE"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    def __str__(self):
        return self.title

class TaskAction(models.Model):
    task = models.ForeignKey(
        Task,
        related_name="actions",
        on_delete=models.CASCADE
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action for Task {self.task_id}"

