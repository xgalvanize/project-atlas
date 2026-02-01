import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import graphql_jwt

User = get_user_model()

# -----------------------------
# User Type
# -----------------------------
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

# -----------------------------
# Register Mutation
# -----------------------------
class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String()

    def mutate(self, info, username, password, email=""):
        if User.objects.filter(username=username).exists():
            raise Exception("Username already taken")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        return RegisterUser(user=user)

# -----------------------------
# Mutation Root
# -----------------------------
class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user
