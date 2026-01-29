# tasks/models.py
from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskAction(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="actions")
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action on {self.task.title}: {self.description[:30]}"
