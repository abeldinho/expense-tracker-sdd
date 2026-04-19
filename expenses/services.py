# apps/expenses/services.py

from .models import Expense
from django.db.models import Sum

def create_expense(data):
    if data["amount"] <= 0:
        raise ValueError("Amount must be greater than 0")

    return Expense.objects.create(**data)


def get_balance(user):
    result = Expense.objects.filter(user=user).aggregate(total=Sum("amount"))
    return result["total"] or 0