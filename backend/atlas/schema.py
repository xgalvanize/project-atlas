import graphene
from projects.schema import ProjectsQuery, ProjectsMutation

class Query(ProjectsQuery, graphene.ObjectType):
    pass

class Mutation(ProjectsMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)


# import graphene

# from projects.schema import ProjectsQuery
# from tasks.schema import TasksQuery


# class Query(
#     ProjectsQuery,
#     TasksQuery,
#     graphene.ObjectType,
# ):
#     hello = graphene.String(default_value="Hello, Atlas")


# schema = graphene.Schema(query=Query)
