from rest_framework import serializers
from .models import Wallet


class WalletSerialiser(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        max_digits=16, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = Wallet
        fields = ["balance"]
