from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserAccountBalance(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    amount = models.BigIntegerField(default=0)


class Transaction(models.Model):

    TRANSACTION_TYPES = (
        (
            'deposit', 'Пополнение'
        ),
        (
            'transfer', 'Перевод средств'
        ),
        (
            'income', 'Получение'
        )
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    related_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    desc = models.CharField(blank=True)

