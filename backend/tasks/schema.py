import graphene
from graphene_django import DjangoObjectType
from .models import Task
from projects.models import Project

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "created_at", "actions")

class CreateTask(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()

    task = graphene.Field(TaskType)

    def mutate(self, info, project_id, title, description=""):
        project = Project.objects.get(pk=project_id)
        task = Task.objects.create(
            project=project,
            title=title,
            description=description,
        )
        return CreateTask(task=task)

class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType)

    def resolve_tasks(root, info):
        return Task.objects.all()

class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()


# import graphene
# from .models import Task, TaskAction
# from graphene_django import DjangoObjectType

# class TaskActionType(DjangoObjectType):
#     class Meta:
#         model = TaskAction
#         fields = ("id", "description", "created_at")


# class TaskType(DjangoObjectType):
#     class Meta:
#         model = Task
#         fields = (
#             "id",
#             "title",
#             "description",
#             "status",      # <-- THIS IS REQUIRED
#             "created_at",
#             "actions",
#         )

# class CreateTaskAction(graphene.Mutation):
#     class Arguments:
#         task_id = graphene.ID(required=True)
#         description = graphene.String(required=True)

#     action = graphene.Field(TaskActionType)

#     def mutate(self, info, task_id, description):
#         task = Task.objects.get(pk=task_id)
#         action = TaskAction.objects.create(
#             task=task,
#             description=description,
#         )
#         return CreateTaskAction(action=action)


# class Mutation(graphene.ObjectType):
#     create_task_action = CreateTaskAction.Field()
