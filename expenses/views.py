from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect

from .serializers import ExpenseSerializer
from .forms import ExpenseForm
from .services import create_expense, get_balance
from .models import Expense
from django.contrib import messages


def create_expense_form(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto registrado correctamente")
            return redirect("/form/")
        messages.warning(request, "Revisa los datos")
        messages.error(request, "Error al guardar")
    else:
        form = ExpenseForm()

    expenses = Expense.objects.all().order_by("-created_at")
    balance = get_balance()

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