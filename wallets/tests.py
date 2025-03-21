from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


from .models import Wallet

# Create your tests here.


class WalletModelTests(TestCase):
    def test_default_balance(self):
        wallet = Wallet.objects.create()
        self.assertEqual(wallet.balance, 0)


class WalletOperationsTest(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(balance=1000)
        self.valid_payload = {"operation_type": "DEPOSIT", "amount": 500}
        self.invalid_payload = {"operation_type": "INVALID", "amount": -100}

    def test_wallet_creation(self):
        self.assertEqual(self.wallet.balance, 1000)
        self.assertTrue(self.wallet.uuid)

    def test_get_balance(self):
        url = reverse("wallet-detail", kwargs={"wallet_uuid": self.wallet.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["balance"], 1000)

    def test_get_wrong_wallet(self):
        url = reverse("wallet-detail", kwargs={"wallet_uuid": "something_wrong"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_deposit_operation(self):
        url = reverse("wallet-operation", kwargs={"wallet_uuid": self.wallet.uuid})
        response = self.client.post(url, self.valid_payload, format="json")
        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.wallet.balance, 1500)
