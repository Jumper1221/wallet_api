from decimal import Decimal
from venv import create
from django.core.serializers import serialize
from django.forms import ValidationError
from rest_framework import views, status
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction

from .models import Wallet, Operation
from .serializers import WalletSerialiser


def index(request):
    return render(request, "wallets/index.html")
    # return HttpResponse("Home page")


class WalletView(views.APIView):
    def get(self, request, wallet_uuid):
        wallet = Wallet.objects.get(id=wallet_uuid)
        serializer = WalletSerialiser(wallet)
        return Response(serializer.data)


class OperationView(views.APIView):
    def post(self, request, wallet_uuid):
        operation_type = request.data.get("operation_type")
        amount = request.data.get("amount")
        try:
            amount = Decimal(amount)
            if amount < 0:
                raise ValidationError("Amount must be zero or bigger")
        except:
            raise ValidationError("Invalid amount")

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(id=wallet_uuid)
            if operation_type == Operation.WITHDRAW:
                if wallet.balance < amount:
                    return Response(
                        {"error": "Not enough funds"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                wallet.balance -= amount
            elif operation_type == Operation.DEPOSIT:
                wallet.balance += amount
            else:
                return Response(
                    {"error": "Invalid operation type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            wallet.save()
            Operation.objects.create(
                wallet=wallet, operation_type=operation_type, amount=amount
            )
            return Response({"balance": wallet.balance})
