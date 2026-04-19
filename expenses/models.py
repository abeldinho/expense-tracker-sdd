# apps/expenses/models.py

from django.db import models
from django.contrib.auth.models import User

class ExpenseType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
