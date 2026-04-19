from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



from .serializers import ExpenseSerializer
from .forms import ExpenseForm
from .services import create_expense, get_balance
from .models import Expense
from django.contrib import messages

@login_required
def create_expense_form(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            form.save()
            messages.success(request, "Gasto registrado correctamente")
            return redirect("expenses:ingresar_expense")
        messages.warning(request, "Revisa los datos")
    else:
        form = ExpenseForm()

    expenses = Expense.objects.filter(user=request.user).order_by("-created_at")
    balance = get_balance(request.user)

    return render(request, "expenses/form.html", {
        "form": form,
        "expenses": expenses,
        "balance": balance
    })

class ExpenseCreateView(APIView):

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        expense = create_expense(serializer.validated_data)

        response_serializer = ExpenseSerializer(expense)

        return Response(
            {
                "mensaje": "Gasto creado correctamente",
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
class ExpenseListView(APIView):

    def get(self, request):
        expenses = Expense.objects.all().order_by("-created_at")
        serializer = ExpenseSerializer(expenses, many=True)

        return Response(
            {
                "mensaje": "Lista de gastos",
                "data": serializer.data
            }
        )

class BalanceView(APIView):

    def get(self, request):
        balance = get_balance()

        return Response(
            {
                "mensaje": "Balance total",
                "data": {
                    "balance": balance
                }
            }
        )

@login_required
def editar_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto actualizado correctamente")
            return redirect("expenses:ingresar_expense")
        messages.error(request, "Error al actualizar el gasto")
    else:
        form = ExpenseForm(instance=expense)

    return render(request, "expenses/edit.html", {"form": form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        expense.delete()
        messages.success(request, "Gasto eliminado correctamente")
        return redirect("expenses:ingresar_expense")

    return render(request, "expenses/delete.html", {"expense": expense})