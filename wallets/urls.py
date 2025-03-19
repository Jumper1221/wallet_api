from django.urls import path
from .views import WalletView

app_name = "wallets"


urlpatterns = [
    path("api/v1/wallets/<uuid:wallet_uuid>", WalletView.as_view()),
]
