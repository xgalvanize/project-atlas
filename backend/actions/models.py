from django.db import models
from tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskAction(models.Model):
    task = models.ForeignKey(Task, related_name="actions", on_delete=models.CASCADE)
    actor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.description[:30]}"
