from api.serializers import AccountSerializer, BalanceUpdateSerializer
from api.models import Account, Transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response

def get_account(account_id):
    try:
        return Account.objects.get(pk=account_id)
    except Account.DoesNotExist:
        return None

@api_view(['PUT'])
def update_balance(request, account_id):
    update_data = BalanceUpdateSerializer(data=request.data)
    if not update_data.is_valid():
        return Response(data="Invalid Update data", status=400)
    account = get_account(account_id)
    if not account:
        return Response(data={"error": f"no account with id: {account_id}"}, content_type="application/json", status=404)

    if update_data.data['action'] == 'TRANSFER' and not update_data.data.get('target_id', None):
        return Response(data={"error": "target_id required for action: TRANSFER"}, content_type="application/json", status=400)

    if update_data.data['action'] == 'TRANSFER':
        if account.balance >= update_data.data['amount']:
            target_id = update_data.data['target_id']
            target = get_account(target_id)
            if not target:
                return Response(data={"error": f"no account with id: {target_id}"}, content_type="application/json", status=404)
            account.balance -= update_data.data['amount']
            target.balance += update_data.data['amount']
            account.save()
            target.save()
            Transaction.objects.create(
                action=update_data.data['action'],
                source=account.username,
                target=target.username,
                amount=update_data.data['amount']
            )
    if update_data.data['action'] == 'DEPOSIT':
        account.balance += update_data.data['amount']
        account.save()
        Transaction.objects.create(
            action=update_data.data['action'],
            source=account.username,
            amount=update_data.data['amount']
        )
    if update_data.data['action'] == 'WITHDRAW':
        if account.balance >= update_data.data['amount']: 
            account.balance -= update_data.data['amount']
            account.save()
            Transaction.objects.create(
                action=update_data.data['action'],
                source=account.username,
                amount=update_data.data['amount']
            )
    
    return Response(data={"done": f"account balance synced"}, content_type="application/json")


@api_view(['GET'])
def list_accounts(request):
    accounts = Account.objects.all()
    accounts_data = AccountSerializer(instance=accounts, many=True)
    return Response(accounts_data.data, content_type="application/json")


@api_view(['GET'])
def get_transactions(request):
    transactions = Transaction.objects.all()
    transaction_strs = [str(transaction) for transaction in transactions]

    return Response(data={"transactions": transaction_strs}, content_type="application/json")
