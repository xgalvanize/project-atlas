import graphene
from graphene_django import DjangoObjectType
from .models import Project

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ("id", "name", "description", "created_at", "tasks")

class CreateProject(graphene.Mutation):
    project = graphene.Field(ProjectType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, name, description=""):
        project = Project.objects.create(name=name, description=description)
        return CreateProject(project=project)



class Query(graphene.ObjectType):
    projects = graphene.List(ProjectType)

    def resolve_projects(root, info):
        return Project.objects.all()

class Mutation(graphene.ObjectType):
    pass

