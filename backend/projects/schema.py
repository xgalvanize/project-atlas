import graphene
from graphene_django import DjangoObjectType
from .models import Project
from tasks.schema import TaskType
from graphql_jwt.decorators import login_required



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
        user = info.context.user

        project = Project.objects.create(
            name=name,
            description=description,
            owner=user,
        )

        return CreateProject(project=project)


class Query(graphene.ObjectType):
    projects = graphene.List(ProjectType)

    @login_required
    def resolve_projects(root, info):
        return Project.objects.filter(owner=info.context.user)


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
