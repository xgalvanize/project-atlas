import graphene
import projects.schema
import tasks.schema
import actions.schema

class Mutation(
    projects.schema.Mutation,
    tasks.schema.Mutation,
    actions.schema.Mutation,
    graphene.ObjectType,
):
    pass

class Query(
    projects.schema.Query,
    tasks.schema.Query,
    actions.schema.Query,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

# import graphene
# from graphene_django import DjangoObjectType
# from projects.models import Project
# from tasks.models import Task, TaskAction
# from tasks.schema import TaskActionType, TaskType
# -----------------------------
# GraphQL Types
# -----------------------------
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


# class ProjectType(DjangoObjectType):
#     class Meta:
#         model = Project
#         fields = ("id", "name", "description", "created_at", "tasks")


# -----------------------------
# Queries
# -----------------------------
# class Query(graphene.ObjectType):
#     projects = graphene.List(ProjectType)
#     tasks = graphene.List(TaskType)

#     def resolve_projects(root, info):
#         return Project.objects.all()

#     def resolve_tasks(root, info):
#         return Task.objects.all()


# -----------------------------
# Mutations
# -----------------------------
# class CreateProject(graphene.Mutation):
#     project = graphene.Field(ProjectType)

#     class Arguments:
#         name = graphene.String(required=True)
#         description = graphene.String()

#     def mutate(self, info, name, description=""):
#         project = Project.objects.create(name=name, description=description)
#         return CreateProject(project=project)


# class CreateTask(graphene.Mutation):
#     task = graphene.Field(TaskType)

#     class Arguments:
#         project_id = graphene.ID(required=True)
#         title = graphene.String(required=True)
#         description = graphene.String()

#     def mutate(self, info, project_id, title, description=""):
#         project = Project.objects.get(pk=project_id)
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
#         task = Task.objects.get(pk=task_id)
#         if title is not None:
#             task.title = title
#         if description is not None:
#             task.description = description
#         if status is not None:
#             task.status = status
#         task.save()
#         return UpdateTask(task=task)


# class Mutation(graphene.ObjectType):
#     create_project = CreateProject.Field()
#     create_task = CreateTask.Field()
#     update_task = UpdateTask.Field()


# -----------------------------
# Final Schema
# -----------------------------
# schema = graphene.Schema(
#     query=Query,
#     mutation=Mutation,
#     types=[ProjectType, TaskType, TaskActionType]  # <-- Force Graphene to use these exact classes
# )

# import graphene
# from projects.models import Project, Task, TaskAction
# from graphene_django import DjangoObjectType

# # -----------------------------
# # GraphQL Types
# # -----------------------------
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
#             "status",      # <-- THIS MUST EXIST
#             "created_at",
#             "actions",
#         )


# class ProjectType(DjangoObjectType):
#     class Meta:
#         model = Project
#         fields = ("id", "name", "description", "created_at", "tasks")


# # -----------------------------
# # Queries
# # -----------------------------
# class Query(graphene.ObjectType):
#     projects = graphene.List(ProjectType)
#     tasks = graphene.List(TaskType)

#     def resolve_projects(root, info):
#         return Project.objects.all()

#     def resolve_tasks(root, info):
#         return Task.objects.all()


# # -----------------------------
# # Mutations
# # -----------------------------
# class CreateProject(graphene.Mutation):
#     project = graphene.Field(ProjectType)

#     class Arguments:
#         name = graphene.String(required=True)
#         description = graphene.String()

#     def mutate(self, info, name, description=""):
#         project = Project.objects.create(name=name, description=description)
#         return CreateProject(project=project)


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

#         if title is not None:
#             task.title = title
#         if description is not None:
#             task.description = description
#         if status is not None:
#             task.status = status

#         task.save()
#         return UpdateTask(task=task)


# class Mutation(graphene.ObjectType):
#     create_project = CreateProject.Field()
#     create_task = CreateTask.Field()
#     update_task = UpdateTask.Field()


# # -----------------------------
# # Schema
# # -----------------------------
# schema = graphene.Schema(
#     query=Query,
#     mutation=Mutation,
#     types=[ProjectType, TaskType, TaskActionType]  # Force Graphene to use these exact classes
# )


# import graphene
# from projects.schema import Query as ProjectsQuery, Mutation as ProjectsMutation

# class Query(ProjectsQuery, graphene.ObjectType):
#     pass

# class Mutation(ProjectsMutation, graphene.ObjectType):
#     pass

# schema = graphene.Schema(query=Query, mutation=Mutation)
