import graphene
from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar
from .tasks import process_action
from .models import Project, Action, Actor, Task
from django.contrib.auth.models import User


# ---------------------
# GraphQL Types
# ---------------------
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

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "is_completed", "created_at")

class ProjectType(DjangoObjectType):
    actions = graphene.List(ActionType)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "created_at", "tasks")

    def resolve_actions(self, info):
        return self.actions.all()


# ---------------------
# Mutations
# ---------------------
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

        # Background processing
        process_action.delay(action.id)

        return CreateAction(action=action)


class UpdateActionStatus(graphene.Mutation):
    class Arguments:
        action_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    action = graphene.Field(ActionType)

    def mutate(self, info, action_id, status):
        action = Action.objects.get(id=action_id)
        action.status = status
        action.save()
        return UpdateActionStatus(action=action)


class AssignActionActor(graphene.Mutation):
    class Arguments:
        action_id = graphene.ID(required=True)
        actor_id = graphene.ID(required=True)

    action = graphene.Field(ActionType)

    def mutate(self, info, action_id, actor_id):
        action = Action.objects.get(id=action_id)
        actor = Actor.objects.get(id=actor_id)
        action.actor = actor
        action.save()
        return AssignActionActor(action=action)

class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, project_id, title, description=""):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise Exception("Project with the given ID does not exist")

        task = Task.objects.create(
            project=project,
            title=title,
            description=description
        )
        return CreateTask(task=task)

class CreateProject(graphene.Mutation):
    project = graphene.Field(ProjectType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, name, description=""):
        project = Project.objects.create(
            name=name,
            description=description
        )
        return CreateProject(project=project)

# ---------------------
# Queries
# ---------------------
class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    all_tasks = graphene.List(TaskType)
    def resolve_all_projects(root, info):
        return Project.objects.all()

    def resolve_all_tasks(root, info):
        return Task.objects.all()
# ---------------------
# Mutation Root
# ---------------------
class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    create_action = CreateAction.Field()
    update_action_status = UpdateActionStatus.Field()
    assign_action_actor = AssignActionActor.Field()
    create_task = CreateTask.Field()
