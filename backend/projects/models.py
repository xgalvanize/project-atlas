from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Action(models.Model):
    """
    Generalized unit of work.
    Domain-agnostic by design.
    """

    action_type = models.CharField(
        max_length=50,
        help_text="Free-form category (assign, deliver, deploy, inspect, etc.)"
    )

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    context = models.JSONField(
        null=True,
        blank=True,
        help_text="Arbitrary structured data for this action"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} [{self.status}]"
