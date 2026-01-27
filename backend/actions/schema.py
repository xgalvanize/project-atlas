import graphene
from graphene_django import DjangoObjectType
from .models import TaskAction
from tasks.models import Task

class TaskActionType(DjangoObjectType):
    class Meta:
        model = TaskAction
        fields = ("id", "task", "actor", "description", "created_at")

class CreateTaskAction(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        description = graphene.String(required=True)

    action = graphene.Field(TaskActionType)

    def mutate(self, info, task_id, description):
        task = Task.objects.get(pk=task_id)
        action = TaskAction.objects.create(
            task=task,
            description=description,
        )
        return CreateTaskAction(action=action)

class Mutation(graphene.ObjectType):
    create_task_action = CreateTaskAction.Field()

class Query(graphene.ObjectType):
    task_actions = graphene.List(TaskActionType)

    def resolve_task_actions(root, info):
        return TaskAction.objects.all()

# import graphene
# from graphene_django import DjangoObjectType
# from .models import TaskAction

# class TaskActionType(DjangoObjectType):
#     class Meta:
#         model = TaskAction
#         fields = ("id", "task", "actor", "description", "created_at")

# Mutation for creating an action
# class CreateTaskAction(graphene.Mutation):
#     class Arguments:
#         task_id = graphene.ID(required=True)
#         description = graphene.String(required=True)

#     action = graphene.Field(TaskActionType)

#     def mutate(self, info, task_id, description):
#         from tasks.models import Task
#         task = Task.objects.get(pk=task_id)
#         action = TaskAction.objects.create(
#             task=task,
#             description=description,
#         )
#         return CreateTaskAction(action=action)


# class Mutation(graphene.ObjectType):
#     create_task_action = CreateTaskAction.Field()
