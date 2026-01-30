import graphene
from graphene_django import DjangoObjectType
from .models import Project
from tasks.schema import TaskType
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectType(DjangoObjectType):
    tasks = graphene.List(TaskType)

    class Meta:
        model = Project
        fields = ("id", "name", "owner", "description", "createdAt")

    def resolve_tasks(self, info):
        return self.tasks.all()

class CreateProject(graphene.Mutation):
    project = graphene.Field(ProjectType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, name, description=""):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        project = Project.objects.create(
            name=name,
            description=description,
            owner=user,
        )
        return CreateProject(project=project)


class Query(graphene.ObjectType):
    projects = graphene.List(ProjectType)

    def resolve_projects(self, info):
        return Project.objects.all()


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
