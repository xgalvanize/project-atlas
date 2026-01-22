import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Project


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")

class ProjectType(DjangoObjectType):
    owner = graphene.Field(UserType)

    class Meta:
        model = Project
        fields = ("id", "name", "owner")


class ProjectsQuery(graphene.ObjectType):
    projects = graphene.List(ProjectType)

    def resolve_projects(root, info):
        return Project.objects.all()
