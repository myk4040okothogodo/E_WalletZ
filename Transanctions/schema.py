import graphene
from .models import Transanction, TransanctionProfile
from graphene_django import DjangoObjectType
from django.contrib.auth import authenticate
from datetime import datetime
from E_WalletZ.authentication import TokenManager
from E_WalletZ.permissions import paginate, is_authenticated
from user_controller.models import User
from Wallet.models import Wallet
from .movemoney import MovingMoney


CONST_TRANSANCTION_FEE_PERCENTAGE = 0.25

class TransanctionType(DjangoObjectType):
    class Meta:
        model = Transanction


class TransanctionProfile(DjangoObjectType):
    class Meta:
        model = TransanctionProfile


class MakeTransanction(graphene.Mutation):
    status  = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        amount_to_send = graphene.Float()
        email = graphene.String()

    @is_authenticated
    def mutate(self, info, email, amount_to_send):
        receiver = User.objects.get(email=email)
        if (receiver.id == info.context.user.id):
            return Exception("Cant send Money to yourself")
        user = User.objects.get(id = info.context.user.id)
        receiver_wallet = Wallet.objects.get(user_id=receiver.id)
        sender_wallet   = Wallet.objects.get(user_id=info.context.user.id)
        if sender_wallet.amount_available <= ((amount_to_send*CONST_TRANSANCTION_FEE_PERCENTAGE)+amount_to_send):
            return Exception(f"You have insufficient funds '{Wallet_user.amount_available}' to complete the cash transfer and pay charges, top up to continue")
        #amount_to_send = graphene.Decimal(amount_to_send)
        try:
            Transanction.objects.create(wallet=sender_wallet,   sender=user, receiver=receiver, amount=amount_to_send)
            Transanction.objects.create(wallet=receiver_wallet, sender=user, receiver=receiver, amount=amount_to_send)
            #MovingMoney.movemoney(info=info, sender=user, receiver=receiver,wallet=Wallet ,amount=amount_to_send)
        except Exception:
            return Exception("Transanction failed please try again")
        MovingMoney.movemoney(info=info, sender=user, receiver=receiver,wallet=Wallet,amount=amount_to_send)
        return MakeTransanction(
            status= True,
            message = f"You have succesfully transfered {amount_to_send} from your wallet to {receiver.email}"
        )



class DeleteTransanction(graphene.Mutation):
    status = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        transanction_id = graphene.ID(required=True)


    @is_authenticated
    def mutate(self, info, transanction_id):
        Wallet = Wallet.objects.get(user_id=info.context.user.id)
        Transanction.object.filter(
            wallet=Wallet,
            id = transanction_id
        ).delete()
        return DeleteTransanction(
            status = True,
            message = f"you have succesfully deleted the transanction {transanction_id}"
        )



class Query(graphene.ObjectType):
    transanctions = graphene.Field(paginate(TransanctionType), page=graphene.Int())

    @is_authenticated
    def resolve_transanctions(self,info):
        wallet = Wallet.objects.get(user_id=info.context.user.id)
        print("Wallet :", wallet)
        return Transanction.objects.filter(wallet_id=wallet.id)



class Mutation(graphene.ObjectType):
    make_transanction = MakeTransanction.Field()
    
    delete_transanction  = DeleteTransanction.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)
