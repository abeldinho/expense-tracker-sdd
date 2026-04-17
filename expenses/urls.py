from django.urls import path
from . import views

urlpatterns = [
    path('gastos/', views.ExpenseCreateView.as_view()),
    path('gastos/listar/', views.ExpenseListView.as_view()),
    path('balance/', views.BalanceView.as_view()),
]