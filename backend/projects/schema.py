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

# import graphene
# from graphene_django import DjangoObjectType
# from .models import Project, Task, TaskAction


# ——————————————————————
# GraphQL Types
# ——————————————————————

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
#             "status",      # <- this line must exist
#             "created_at",
#             "actions",
#         )


# class ProjectType(DjangoObjectType):
#     class Meta:
#         model = Project
#         fields = ("id", "name", "description", "created_at", "tasks")


# ——————————————————————
# Queries
# ——————————————————————

# class Query(graphene.ObjectType):
#     projects = graphene.List(ProjectType)
#     tasks = graphene.List(TaskType)

#     def resolve_projects(root, info):
#         return Project.objects.all()

#     def resolve_tasks(root, info):
#         return Task.objects.all()


# ——————————————————————
# Mutations
# ——————————————————————


# class CreateTask(graphene.Mutation):
#     task = graphene.Field(TaskType)

#     class Arguments:
#         project_id = graphene.ID(required=True)
#         title = graphene.String(required=True)
#         description = graphene.String()

#     def mutate(self, info, project_id, title, description=""):
#         try:
#             project = Project.objects.get(pk=project_id)
#         except Project.DoesNotExist:
#             raise Exception("Invalid project ID")

#         task = Task.objects.create(
#             project=project,
#             title=title,
#             description=description
#         )
#         return CreateTask(task=task)


# class UpdateTask(graphene.Mutation):
#     task = graphene.Field(TaskType)

#     class Arguments:
#         task_id = graphene.ID(required=True)
#         title = graphene.String()
#         description = graphene.String()
#         status = graphene.String()

#     def mutate(self, info, task_id, title=None, description=None, status=None):
#         try:
#             task = Task.objects.get(pk=task_id)
#         except Task.DoesNotExist:
#             raise Exception("Invalid task ID")

#         changes = []

#         if title is not None and title != task.title:
#             changes.append(f'Title changed from "{task.title}" to "{title}"')
#             task.title = title

#         if description is not None and description != task.description:
#             changes.append("Description updated")
#             task.description = description

#         if status is not None and status != task.status:
#             changes.append(f"Status changed from {task.status} to {status}")
#             task.status = status

#         task.save()

#         # Log automatic actions
#         for change in changes:
#             TaskAction.objects.create(task=task, description=change)

#         return UpdateTask(task=task)


# class CreateTaskAction(graphene.Mutation):
#     action = graphene.Field(TaskActionType)

#     class Arguments:
#         task_id = graphene.ID(required=True)
#         description = graphene.String(required=True)

#     def mutate(self, info, task_id, description):
#         try:
#             task = Task.objects.get(pk=task_id)
#         except Task.DoesNotExist:
#             raise Exception("Invalid task ID")

#         action = TaskAction.objects.create(task=task, description=description)
#         return CreateTaskAction(action=action)


# class Mutation(graphene.ObjectType):
#     create_project = CreateProject.Field()
#     create_task = CreateTask.Field()
#     update_task = UpdateTask.Field()
#     create_task_action = CreateTaskAction.Field()

# import graphene
# from graphene_django import DjangoObjectType
# from graphene.types.generic import GenericScalar
# from .tasks import process_action
# from .models import Project, Action, Actor, Task, TaskAction
# from django.contrib.auth.models import User


# # ---------------------
# # GraphQL Types
# # ---------------------
# class UserType(DjangoObjectType):
#     class Meta:
#         model = User
#         fields = ("id", "username")


# class ActorType(DjangoObjectType):
#     class Meta:
#         model = Actor
#         fields = ("id", "name", "role", "user")


# class ActionType(DjangoObjectType):
#     context = GenericScalar()

#     class Meta:
#         model = Action
#         fields = ("id", "action_type", "status", "context", "actor", "created_at")

# class TaskType(DjangoObjectType):
#     class Meta:
#         model = Task
#         fields = (
#             "id",
#             "title",
#             "description",
#             "status",
#             "created_at",
#             "actions",
#         )



# class ProjectType(DjangoObjectType):
#     actions = graphene.List(ActionType)

#     class Meta:
#         model = Project
#         fields = ("id", "name", "description", "created_at", "tasks")

#     def resolve_actions(self, info):
#         return self.actions.all()

# class TaskActionType(DjangoObjectType):
#     class Meta:
#         model = TaskAction
#         fields = ("id", "description", "created_at")

# # ---------------------
# # Mutations
# # ---------------------
# class CreateAction(graphene.Mutation):
#     class Arguments:
#         project_id = graphene.ID(required=True)
#         action_type = graphene.String(required=True)
#         status = graphene.String(required=False)
#         context = GenericScalar(required=False)
#         actor_id = graphene.ID(required=False)

#     action = graphene.Field(ActionType)

#     def mutate(self, info, project_id, action_type, status="pending", context=None, actor_id=None):
#         project = Project.objects.get(id=project_id)

#         actor = None
#         if actor_id:
#             actor = Actor.objects.get(id=actor_id)

#         action = Action.objects.create(
#             project=project,
#             action_type=action_type,
#             status=status,
#             context=context or {},
#             actor=actor
#         )

#         # Background processing
#         process_action.delay(action.id)

#         return CreateAction(action=action)


# class UpdateActionStatus(graphene.Mutation):
#     class Arguments:
#         action_id = graphene.ID(required=True)
#         status = graphene.String(required=True)

#     action = graphene.Field(ActionType)

#     def mutate(self, info, action_id, status):
#         action = Action.objects.get(id=action_id)
#         action.status = status
#         action.save()
#         return UpdateActionStatus(action=action)


# class AssignActionActor(graphene.Mutation):
#     class Arguments:
#         action_id = graphene.ID(required=True)
#         actor_id = graphene.ID(required=True)

#     action = graphene.Field(ActionType)

#     def mutate(self, info, action_id, actor_id):
#         action = Action.objects.get(id=action_id)
#         actor = Actor.objects.get(id=actor_id)
#         action.actor = actor
#         action.save()
#         return AssignActionActor(action=action)

# class CreateTask(graphene.Mutation):
#     task = graphene.Field(TaskType)

#     class Arguments:
#         project_id = graphene.ID(required=True)
#         title = graphene.String(required=True)
#         description = graphene.String()

#     def mutate(self, info, project_id, title, description=""):
#         try:
#             project = Project.objects.get(pk=project_id)
#         except Project.DoesNotExist:
#             raise Exception("Project with the given ID does not exist")

#         task = Task.objects.create(
#             project=project,
#             title=title,
#             description=description
#         )
#         return CreateTask(task=task)

# class UpdateTask(graphene.Mutation):
#     task = graphene.Field(TaskType)

#     class Arguments:
#         task_id = graphene.ID(required=True)
#         title = graphene.String()
#         description = graphene.String()
#         is_completed = graphene.Boolean()

#     def mutate(self, info, task_id, title=None, description=None, is_completed=None):
#         try:
#             task = Task.objects.get(pk=task_id)
#         except Task.DoesNotExist:
#             raise Exception("Task with the given ID does not exist")

#         if title is not None:
#             task.title = title
#         if description is not None:
#             task.description = description
#         if is_completed is not None:
#             task.is_completed = is_completed

#         task.save()
#         return UpdateTask(task=task)


# class CreateProject(graphene.Mutation):
#     project = graphene.Field(ProjectType)

#     class Arguments:
#         name = graphene.String(required=True)
#         description = graphene.String()

#     def mutate(self, info, name, description=""):
#         project = Project.objects.create(
#             name=name,
#             description=description
#         )
#         return CreateProject(project=project)

# class CreateTaskAction(graphene.Mutation):
#     action = graphene.Field(TaskActionType)

#     class Arguments:
#         task_id = graphene.ID(required=True)
#         description = graphene.String(required=True)

#     def mutate(self, info, task_id, description):
#         try:
#             task = Task.objects.get(pk=task_id)
#         except Task.DoesNotExist:
#             raise Exception("Task does not exist")

#         action = TaskAction.objects.create(
#             task=task,
#             description=description
#         )
#         return CreateTaskAction(action=action)


# # ---------------------
# # Queries
# # ---------------------
# class Query(graphene.ObjectType):
#     projects = graphene.List(ProjectType)
#     tasks = graphene.List(TaskType)
#     def resolve_all_projects(root, info):
#         return Project.objects.all()

#     def resolve_all_tasks(root, info):
#         return Task.objects.all()
# # ---------------------
# # Mutation Root
# # ---------------------
# class Mutation(graphene.ObjectType):
#     create_project = CreateProject.Field()
#     create_action = CreateAction.Field()
#     update_action_status = UpdateActionStatus.Field()
#     assign_action_actor = AssignActionActor.Field()
#     create_task = CreateTask.Field()
#     update_task = UpdateTask.Field()
#     create_task_action = CreateTaskAction.Field()
