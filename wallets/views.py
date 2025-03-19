from django.core.serializers import serialize
from rest_framework import views
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse

from .models import Wallet
from .serializers import WalletSerialiser


def index(request):
    return render(request, "wallets/index.html")
    # return HttpResponse("Home page")


class WalletView(views.APIView):
    def get(self, request, wallet_uuid):
        wallet = Wallet.objects.get(id=wallet_uuid)
        serializer = WalletSerialiser(wallet)
        return Response(serializer.data)
