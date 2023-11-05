import graphene

from user_controller.schema import schema as user_schema
from Transanctions.schema import schema as transanction_schema
from Wallet.schema  import schema as wallet_schema


class Query(user_schema.Query, transanction_schema.Query, wallet_schema.Query, graphene.ObjectType):
    pass


class Mutation(user_schema.Mutation, transanction_schema.Mutation, wallet_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
