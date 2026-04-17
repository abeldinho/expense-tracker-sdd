from django.urls import path
from . import views

urlpatterns = [
    path('gastos/', views.ExpenseCreateView.as_view()),
    path('gastos/listar/', views.ExpenseListView.as_view()),
    path('ingresar/', views.create_expense_form),
    path('balance/', views.BalanceView.as_view()),
]