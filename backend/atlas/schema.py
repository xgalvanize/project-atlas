import graphene
import projects.schema
import tasks.schema
import users.schema
import graphql_jwt

class Query(
    projects.schema.Query,
    tasks.schema.Query,
    users.schema.Query,
    graphene.ObjectType,
):
    pass

class Mutation(
    projects.schema.Mutation,
    tasks.schema.Mutation,
    users.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
