import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphene.types.generic import GenericScalar

from .models import Project, Action, Actor


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")

class ActorType(DjangoObjectType):
    class Meta:
        model = Actor
        fields = ("id", "name", "role", "user")

class ActionType(DjangoObjectType):
    context = GenericScalar()

    class Meta:
        model = Action
        fields = ("id", "action_type", "status", "context", "actor", "created_at")

class ProjectType(DjangoObjectType):
    actions = graphene.List(ActionType)

    class Meta:
        model = Project
        fields = ("id", "name", "owner", "actions")

    def resolve_actions(self, info):
        return self.actions.all()

class CreateAction(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        action_type = graphene.String(required=True)
        status = graphene.String(required=False)
        context = GenericScalar(required=False)
        actor_id = graphene.ID(required=False)

    action = graphene.Field(ActionType)

    def mutate(self, info, project_id, action_type, status="pending", context=None, actor_id=None):
        project = Project.objects.get(id=project_id)
        actor = None
        if actor_id:
            actor = Actor.objects.get(id=actor_id)

        action = Action.objects.create(
            project=project,
            action_type=action_type,
            status=status,
            context=context or {},
            actor=actor
        )

        return CreateAction(action=action)

# class CreateAction(graphene.Mutation):
#     class Arguments:
#         project_id = graphene.ID(required=True)
#         action_type = graphene.String(required=True)
#         status = graphene.String(required=False)
#         context = GenericScalar(required=False)


#     action = graphene.Field(ActionType)

#     def mutate(self, info, project_id, action_type, status="pending", context=None):
#         project = Project.objects.get(id=project_id)

#         action = Action.objects.create(
#             project=project,
#             action_type=action_type,
#             status=status,
#             context=context or {}
#         )

#         return CreateAction(action=action)


class ProjectsQuery(graphene.ObjectType):
    projects = graphene.List(ProjectType)

    def resolve_projects(root, info):
        return Project.objects.all()

class ProjectsMutation(graphene.ObjectType):
    create_action = CreateAction.Field()
