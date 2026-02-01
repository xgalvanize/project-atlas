import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Project
from tasks.schema import TaskType


class ProjectType(DjangoObjectType):
    tasks = graphene.List(TaskType)

    class Meta:
        model = Project
        fields = ("id", "name", "owner", "description", "created_at")

    def resolve_tasks(self, info):
        return self.tasks.all()


class CreateProject(graphene.Mutation):
    project = graphene.Field(ProjectType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    @login_required
    def mutate(self, info, name, description=""):
        print("USER:", info.context.user)
        print("AUTH:", info.context.user.is_authenticated)

        project = Project.objects.create(
            name=name,
            description=description,
            owner=info.context.user,
        )
        return CreateProject(project=project)


class Query(graphene.ObjectType):
    projects = graphene.List(ProjectType)

    @login_required
    def resolve_projects(self, info):
        return Project.objects.filter(owner=info.context.user)


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
