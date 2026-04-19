from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path('gastos/', views.ExpenseCreateView.as_view(),name='gastos'),
    path('gastos/listar/', views.ExpenseListView.as_view(),name='listar'),
    path('ingresar/', views.create_expense_form,name='ingresar_expense'),
    path('balance/', views.BalanceView.as_view(),name='balance'),
    path('editar/<int:pk>/', views.editar_expense, name='editar_expense'),
    path('eliminar/<int:pk>/', views.delete_expense, name='eliminar_expense'),
]