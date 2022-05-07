from importlib.metadata import requires
from typing_extensions import Required
from rest_framework import serializers

class BalanceUpdateSerializer(serializers.Serializer):
    balance = serializers.FloatField()
    action = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW', 'TRANSFER'])
    target = serializers.CharField(required=False, max_length=255)