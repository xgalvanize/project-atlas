from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Actor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name

class Action(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="actions")
    action_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    context = models.JSONField(default=dict, blank=True)
    actor = models.ForeignKey(Actor, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_actions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} ({self.status})"
