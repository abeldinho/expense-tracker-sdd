import pytest
from rest_framework.test import APIClient
from expenses.models import ExpenseType

@pytest.mark.django_db
def test_create_expense():
    client = APIClient()

    expense_type = ExpenseType.objects.create(name="comida")

    data = {
        "amount": 10000,
        "description": "Almuerzo",
        "expense_type": expense_type.id
    }

    response = client.post("/api/gastos/", data, format="json")

    assert response.status_code == 201
    assert response.data["data"]["amount"] == "10000.00"