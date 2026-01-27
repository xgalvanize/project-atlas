from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# class Task(models.Model):
#     project = models.ForeignKey(
#         Project,
#         related_name="tasks",
#         on_delete=models.CASCADE
#     )
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     is_completed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Status(models.TextChoices):
#         PENDING = "PENDING"
#         IN_PROGRESS = "IN_PROGRESS"
#         DONE = "DONE"

#     status = models.CharField(
#         max_length=20,
#         choices=Status.choices,
#         default=Status.PENDING
#     )
#     def __str__(self):
#         return self.title

class Actor(models.Model):
    """
    Represents a person, volunteer, or organization that can perform actions.
    """
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=50, default="volunteer")  # e.g., volunteer, staff, org

    def __str__(self):
        return f"{self.name} ({self.role})"

class Action(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="actions")
    action_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="pending")
    context = models.JSONField(default=dict, blank=True)
    actor = models.ForeignKey(Actor, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_actions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} ({self.status})"
    
# class TaskAction(models.Model):
#     task = models.ForeignKey(
#         Task,
#         related_name="actions",
#         on_delete=models.CASCADE
#     )
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Action for Task {self.task_id}"
