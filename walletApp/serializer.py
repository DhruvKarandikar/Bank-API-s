from rest_framework import serializers
from .models import Transaction, Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('account_no', 'balance')


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['account', 'transaction_type', 'transaction_balance']



