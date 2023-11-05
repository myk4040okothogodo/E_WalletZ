from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from decimal import Decimal
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
#from Transanctions.models import  Transanction


User = get_user_model()

# Create your models here.

class Wallet(models.Model):
    user = models.OneToOneField(User, related_name="user_wallet", on_delete=models.PROTECT)
    """ amount_available = MoneyField(
            max_digits=11, decimal_places=2, default=0, default_currency='KES',
            validators=[
                MinMoneyValidator(Decimal(0.00)), MaxMoneyValidator(Decimal(999999999.99)),
                ]
            )
    """
    amount_available =  models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.firstName}-{self.user.lastName}-wallet"




class WalletProfile(models.Model):

    TYPES = {
            (0, "Mini"),
            (1, "Regular"),
            (2, "Super"),
            }

    LIMITS = {
            (0, 100000),
            (1, 1000000),
            (2, 100000000),
            (3, 9999999999.99)
            }
    name  = models.PositiveSmallIntegerField(default=1, choices=TYPES)
    limit = models.PositiveSmallIntegerField(default=1, choices=LIMITS)
    wallet = models.OneToOneField(Wallet, related_name="wallet_profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name}-WithLimit-{self.limit}"
