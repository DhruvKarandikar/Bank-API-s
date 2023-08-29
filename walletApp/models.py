from django.db import models
from user.models import User


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    account_no = models.IntegerField()
    balance = models.FloatField(default=0.00)


class Transaction(models.Model):
    class TransactionType(models.IntegerChoices):
        DEPOSIT = 1, 'Deposit'
        WITHDRAWAL = 2, 'Withdrawal'

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_id')
    transaction_type = models.IntegerField(choices=TransactionType.choices)
    transaction_balance = models.FloatField(default=0)
    balance = models.FloatField(default=0.00)


