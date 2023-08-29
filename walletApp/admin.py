from django.contrib import admin
from .models import Transaction, Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'account_no', 'balance']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'transaction_type', 'transaction_balance', 'balance']
