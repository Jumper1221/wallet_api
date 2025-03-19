from rest_framework import serializers
from .models import Wallet


class WalletSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "balance", "created_at"]
