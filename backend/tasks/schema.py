import graphene
from graphene_django import DjangoObjectType
from .models import Task
from projects.models import Project

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "created_at", "actions")

class CreateTask(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()

    task = graphene.Field(TaskType)

    def mutate(self, info, project_id, title, description=""):
        project = Project.objects.get(pk=project_id)
        task = Task.objects.create(
            project=project,
            title=title,
            description=description,
        )
        return CreateTask(task=task)

class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType)

    def resolve_tasks(root, info):
        return Task.objects.all()

class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()


