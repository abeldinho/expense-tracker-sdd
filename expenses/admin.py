from django.contrib import admin
from .models import Expense, ExpenseType

# Register your models here.
@admin.register(Expense)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'created_at','expense_type')