import threading
import uuid
from decimal import Decimal

from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.db import transaction, connection
from rest_framework.test import APITestCase

from .models import Wallet

# Create your tests here.


class WalletModelTests(TestCase):
    def test_default_balance(self):
        wallet = Wallet.objects.create()
        self.assertEqual(wallet.balance, Decimal("0.00"))


class WalletOperationsTest(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(balance=1000)
        self.valid_deposit = {"operation_type": "DEPOSIT", "amount": 500}
        self.valid_withdraw = {"operation_type": "WITHDRAW", "amount": 300}
        self.invalid_payload = {"operation_type": "INVALID", "amount": -100}

    def test_wallet_creation(self):
        self.assertEqual(self.wallet.balance, Decimal("1000.00"))
        self.assertTrue(self.wallet.id)

    def test_get_balance(self):
        url = reverse("wallet-detail", kwargs={"wallet_uuid": self.wallet.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(response.data["balance"]), Decimal("1000.00"))

    def test_get_wrong_wallet(self):
        fake_uuid = uuid.uuid4()
        url = reverse("wallet-detail", kwargs={"wallet_uuid": str(fake_uuid)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_deposit_operation(self):
        url = reverse("wallet-operation", kwargs={"wallet_uuid": self.wallet.id})
        response = self.client.post(url, self.valid_deposit, format="json")
        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.wallet.balance, Decimal("1500.00"))

    def test_withdraw_operation(self):
        url = reverse("wallet-operation", kwargs={"wallet_uuid": self.wallet.id})
        response = self.client.post(url, self.valid_withdraw, format="json")
        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.wallet.balance, Decimal("700.00"))

    def test_invalid_operation(self):
        url = reverse("wallet-operation", kwargs={"wallet_uuid": self.wallet.id})
        response = self.client.post(url, self.invalid_payload, format="json")
        self.assertEqual(response.status_code, 400)


class WalletConcurrencyTests(TransactionTestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(balance=1000)

    def test_concurrent_deposits(self):
        initial_balance = self.wallet.balance
        num_requests = 5
        threads = []

        def make_deposit():
            from django.db import connection

            connection.close()
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(id=self.wallet.id)
                wallet.balance += Decimal("100")
                wallet.save()

        for _ in range(num_requests):
            thread = threading.Thread(target=make_deposit)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.wallet.refresh_from_db()
        self.assertEqual(
            self.wallet.balance, initial_balance + Decimal(num_requests * 100)
        )

    def test_concurrent_withdrawals(self):
        self.wallet.balance = 1000
        self.wallet.save()
        num_requests = 5
        threads = []

        def make_withdrawal():
            from django.db import connection

            connection.close()
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(id=self.wallet.id)
                if wallet.balance >= Decimal("100"):
                    wallet.balance -= Decimal("100")
                    wallet.save()

        for _ in range(num_requests):
            thread = threading.Thread(target=make_withdrawal)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("500.00"))
