import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Project, Action


class ActionType(DjangoObjectType):
    class Meta:
        model = Action
        fields = "__all__"


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
    # Projects
    projects = graphene.List(ProjectType)

    def resolve_projects(self, info):
        return Project.objects.all()

    # Actions
    actions = graphene.List(ActionType)

    def resolve_actions(self, info):
        return Action.objects.all()
