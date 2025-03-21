from django.urls import path
from .views import WalletView, OperationView

app_name = "wallets"


urlpatterns = [
    path(
        "api/v1/wallets/<uuid:wallet_uuid>", WalletView.as_view(), name="wallet-detail"
    ),
    path(
        "api/v1/wallets/<uuid:wallet_uuid>/operation",
        OperationView.as_view(),
        name="wallet-operation",
    ),
]
