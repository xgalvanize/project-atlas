import graphene
from graphene_django import DjangoObjectType
from .models import Task
from projects.models import Project


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "created_at",
            "project",
        )


class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, project_id, title, description=""):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Authentication required")

        project = Project.objects.get(id=project_id)

        task = Task.objects.create(
            project=project,
            title=title,
            description=description,
            created_by=user,
        )

        return CreateTask(task=task)


class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType, project_id=graphene.ID())

    def resolve_tasks(self, info, project_id=None):
        if project_id:
            return Task.objects.filter(project_id=project_id)
        return Task.objects.all()


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
