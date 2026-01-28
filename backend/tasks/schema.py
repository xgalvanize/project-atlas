import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Task
from projects.models import Project
User = get_user_model()
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")  # whatever fields you want exposed

class TaskType(DjangoObjectType):
    createdBy = graphene.Field(lambda: UserType)
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "created_at",
            "created_by",
            "project",
        )
    def resolve_createdBy(self, info):
        return self.created_by


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

class UpdateTaskStatus(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        task_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    def mutate(self, info, task_id, status):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        task = Task.objects.get(id=task_id)

        task.status = status
        task.save()

        return UpdateTaskStatus(task=task)


class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType, project_id=graphene.ID())

    def resolve_tasks(self, info, project_id=None):
        if project_id:
            return Task.objects.filter(project_id=project_id)
        return Task.objects.all()


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task_status = UpdateTaskStatus.Field()
