import graphene
from .models import Wallet, WalletProfile
from graphene_django import DjangoObjectType
from django.contrib.auth import authenticate
from datetime import datetime
from E_WalletZ.authentication import TokenManager
from E_WalletZ.permissions import paginate, is_authenticated
#from django.utils import timezone
#from django.conf import settings
from decimal import Decimal
from graphql.language import ast
from django.contrib.auth import get_user_model


User = get_user_model()



class WalletType(DjangoObjectType):
    class Meta:
        model = Wallet


class WalletProfileType(DjangoObjectType):
    class Meta:
        model = WalletProfile



class RegisterWallet(graphene.Mutation):
    status  = graphene.Boolean()
    message = graphene.String()

    @is_authenticated
    def mutate(self, info, **kwargs):

        user = User.objects.get(id=info.context.user.id)
        Wallet.objects.create(user=user)

        return RegisterWallet(
            status= True,
            message = "Success! Wallet Created ,"
        )


class CreditWallet(graphene.Mutation):
    status = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        credit_amount = graphene.Float()
    
    @is_authenticated
    def mutate(self, info, credit_amount, **kwargs):
        #credit_amount = graphene.Decimal(credit_amount)
        wallet = Wallet.objects.get(user_id=info.context.user.id)
        wallet.amount_available +=  Decimal(str(credit_amount))
        wallet.save()

        return CreditWallet(
            status  = True,
            message = f"Your Wallet has been successfully credited with the amount {credit_amount}"
        )



class DeleteUserWallet(graphene.Mutation):
    status = graphene.Boolean()

    @is_authenticated
    def mutate(self, info, **kwargs):
        Wallet.objects.filter(user_id=info.context.user.id).delete()
        return DeleteUserWallet(
            status = True
        )


class Query(graphene.ObjectType):
    wallet = graphene.Field(paginate(WalletType), page = graphene.Int())
    
    @is_authenticated
    def resolve_wallet(self, info):
        return Wallet.objects.filter(user_id=info.context.user.id)



class Mutation(graphene.ObjectType):
    register_wallet   = RegisterWallet.Field()
    credit_wallet     = CreditWallet.Field()
    delete_user_wallet = DeleteUserWallet.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)
