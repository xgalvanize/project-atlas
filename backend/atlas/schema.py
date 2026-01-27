import graphene
import projects.schema
import tasks.schema
import actions.schema

class Query(
    projects.schema.Query,
    tasks.schema.Query,
    actions.schema.Query,
    graphene.ObjectType,
):
    pass

class Mutation(
    projects.schema.Mutation,
    tasks.schema.Mutation,
    actions.schema.Mutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
