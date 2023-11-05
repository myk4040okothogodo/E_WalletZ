class MovingMoney:

    @staticmethod
    def movemoney(info,sender,receiver,wallet,amount):
        from Wallet.models import Wallet
        import decimal

        print(f"Cash transfer of {amount} from you to {receiver.first_name}-{receiver.last_name} starting")
        
        try:
            sender_wallet = Wallet.objects.get(user_id=sender.id)
            sender_wallet.amount_available   = (sender_wallet.amount_available - decimal.Decimal(str(amount)).quantize(decimal.Decimal('.01')))
            sender_wallet.save()

        except Exception:
            return Exception("Updating of the senders amount_available failed")
        
     
        try:
            receiver_wallet = Wallet.objects.get(user_id = receiver.id)
            receiver_wallet.amount_available = (receiver_wallet.amount_available + decimal.Decimal(str(amount)).quantize(decimal.Decimal('.01')))
            receiver_wallet.save()

        except Exception:
            sender_wallet.amount_available = (sender_wallet.amount_available + decimal.Decimal(str(amount)).quantize(decimal.Decimal('.01')))
            return Exception("Money transfer to receiver has failed")
        
        
        print ("Money Transfer is now complete!")

