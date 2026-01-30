# tasks/schema.py
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Task, Action
from projects.models import Project

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class ActionType(DjangoObjectType):
    createdBy = graphene.Field(UserType)
    class Meta:
        model = Action
        fields = ("id", "description", "createdAt", "createdBy")
    def resolve_createdBy(self, info):
        return self.createdBy

class TaskType(DjangoObjectType):
    createdBy = graphene.Field(UserType)
   
    actions = graphene.List(ActionType)

    def resolve_actions(self, info):
        return self.actions.all()


    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "createdAt", "createdBy", "project")

    def resolve_createdBy(self, info):
        return self.createdBy


# Mutations

class UpdateTaskStatus(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        taskId = graphene.ID(required=True)
        status = graphene.String(required=True)

    def mutate(self, info, taskId, status):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        task = Task.objects.get(id=taskId)
        task.status = status
        task.save()
        return UpdateTaskStatus(task=task)

class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        projectId = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, projectId, title, description=""):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        project = Project.objects.get(id=projectId)
        task = Task.objects.create(
            project=project,
            title=title,
            description=description,
            createdBy=user
        )
        return CreateTask(task=task)

class CreateAction(graphene.Mutation):
    action = graphene.Field(ActionType)

    class Arguments:
        taskId = graphene.ID(required=True)
        description = graphene.String(required=True)

    def mutate(self, info, taskId, description):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        task = Task.objects.get(id=taskId)
        action = Action.objects.create(
            task=task,
            description=description,
            createdBy=user
        )
        return CreateAction(action=action)

# Root schema

class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType, projectId=graphene.ID())

    def resolve_tasks(self, info, projectId=None):
        if projectId:
            return Task.objects.filter(projectId=projectId)
        return Task.objects.all()

class Mutation(graphene.ObjectType):
    createTask = CreateTask.Field()
    updateTaskStatus = UpdateTaskStatus.Field()
    createAction = CreateAction.Field()
