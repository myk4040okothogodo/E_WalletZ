from django.db import models
from django.contrib.auth import get_user_model
from user_controller.models import User
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from decimal import Decimal
from djmoney.models.fields import MoneyField
from Wallet.models import Wallet


transactee = get_user_model()

class Transanction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name="transanction_wallet", on_delete=models.PROTECT)
    sender   = models.OneToOneField(transactee, related_name="sender_transanction", on_delete=models.PROTECT)
    receiver = models.OneToOneField(transactee, related_name="receiver_transanction", on_delete=models.PROTECT)
    """amount  =  MoneyField(
                max_digits=7, decimal_places=2, default=0, default_currency='KES',
                validators=[
                    MinMoneyValidator(Decimal(0.00)), MaxMoneyValidator(Decimal(99999.99))
                ]
            )
    """
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.firstName}_{self.sender.lastName}-to-{self.receiver.firstName}_{self.receiver.lastName}={self.amount}-{self.created_on}"



class TransanctionProfile(models.Model):
    TYPE = {
    (0, "AFRICA"),
    (1, "KENYA"),
    (2, "WORLD")
    }

    CATEGORY = {
    (0, "0 - 100,000"),
    (1, "100,000 - 1,000,000"),
    (2, "1,000,000 - 100,000,000"),
    (3, "100,000,000 - 500,000,000"),
    (4, "> 500,000,000")
    }

    transanction = models.OneToOneField(Transanction, related_name="transanction_profile", on_delete=models.CASCADE)
    transanction_category = models.PositiveSmallIntegerField(default=0, choices=CATEGORY)
    transanction_type     = models.PositiveSmallIntegerField(default=1, choices=TYPE)
    

    def __str__(self):
        return f"{self.transanction_category}-{self.transanction_type}"
