import pytest
from rest_framework.test import APIClient
from expenses.models import Expense, ExpenseType

@pytest.mark.django_db
def test_get_balance():
    client = APIClient()

    expense_type = ExpenseType.objects.create(name="comida")

    Expense.objects.create(amount=10000, description="A", expense_type=expense_type)
    Expense.objects.create(amount=5000, description="B", expense_type=expense_type)

    response = client.get("/api/balance/")

    assert response.status_code == 200
    assert response.data["data"]["balance"] == 15000