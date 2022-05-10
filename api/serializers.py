from rest_framework import serializers

class BalanceUpdateSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    action = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW', 'TRANSFER'])
    target_id = serializers.CharField(required=False, max_length=255)

class AccountSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    balance = serializers.FloatField()

class GetTransactions(serializers.Serializer):
    transactions = serializers.ListField()
