from rest_framework.decorators import api_view
from atm.settings import SECRET_KEY
from user.models import User
from .serializer import TransactionSerializer, AccountSerializer
from .models import Transaction, Account
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import requests

# THIRD_API_URL = "https://www.gov.uk/bank-holidays.json"


@swagger_auto_schema(method="post", request_body=TransactionSerializer,
                     responses={"200": 'TransactionSerializer'}, operation_id="user signup transaction", )
@api_view(['POST'])
def transaction(request):
    # response = requests.get(url=THIRD_API_URL)
    # all read and update of balance logic here from this API
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():

        transaction_type = serializer.validated_data['transaction_type']
        acc_id = serializer.validated_data['account']
        tran_bal = serializer.validated_data['transaction_balance']
        if transaction_type == Transaction.TransactionType.DEPOSIT:
            try:
                acc_balance = Account.objects.get(id=acc_id.id, user_id=request.user.id)
            except Account.DoesNotExist:
                return Response({"error": "account not found"}, 400)  #  Response({'msg': response})
            acc_balance.balance = acc_balance.balance + tran_bal
            acc_balance.save()
            serializer.save()
            return Response({'msg': 'Account updated'})
        if transaction_type == Transaction.TransactionType.WITHDRAWAL:
            try:
                acc_balance = Account.objects.get(id=acc_id.id, user_id=request.user.id)
            except Account.DoesNotExist:
                return Response({"error": "account not found"}, 400)
            acc_balance.balance = acc_balance.balance - tran_bal
            acc_balance.save()
            serializer.save()
            return Response({'msg': 'Account updated'})
        return Response(serializer.data)
    return Response(serializer.errors)


@swagger_auto_schema(method="get",  # request_body=AccountSerializer,
                     responses={"200": 'AccountSerializer'}, operation_id="user get balance get")
@api_view(['GET'])
def get_balance(request):
    # To show the current balance to user from this API

    acc_obj = Account.objects.get(user=request.user)
    serializer = AccountSerializer(acc_obj, many=False)
    return Response({'msg': serializer.data})
