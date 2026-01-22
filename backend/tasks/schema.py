import graphene
from graphene_django import DjangoObjectType
from .models import Task


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"


class TasksQuery(graphene.ObjectType):
    tasks = graphene.List(TaskType)

    def resolve_tasks(self, info):
        return Task.objects.all()
