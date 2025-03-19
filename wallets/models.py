from email.policy import default
import uuid
from django.db import models

# Create your models here.


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Operation(models.Model):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    OPERATION_CHOICES = [
        (DEPOSIT, "Deposit"),
        (WITHDRAW, "Withdraw"),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    created_time = models.DateTimeField(auto_now_add=True)
