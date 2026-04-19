from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth
from .serializers import ExpenseSerializer
from .forms import ExpenseForm
from .services import create_expense, get_balance
from .models import Expense, ExpenseType
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
    categories = ExpenseType.objects.all()

    return render(request, "expenses/form.html", {
        "form": form,
        "expenses": expenses,
        "balance": balance,
        "categorias": categories
    })

@login_required
def expense_dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    categories = ExpenseType.objects.all()

    # 🔎 filtros
    categoria_id = request.GET.get('categoria')
    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')

    if categoria_id:
        expenses = expenses.filter(expense_type_id=categoria_id)

    if fecha_desde:
        expenses = expenses.filter(created_at__gte=fecha_desde)

    if fecha_hasta:
        expenses = expenses.filter(created_at__lte=fecha_hasta)

    # 📊 PIE (por categoría)
    pie_data = (
        expenses.values('expense_type__name')
        .annotate(total=Sum('amount'))
    )

    pie_labels = [d['expense_type__name'] for d in pie_data]
    pie_totals = [float(d['total']) for d in pie_data]

    # 📈 LINEA (por mes)
    monthly_data = (
        expenses
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    line_labels = [d['month'].strftime("%Y-%m") for d in monthly_data]
    line_totals = [float(d['total']) for d in monthly_data]

    context = {
        'expenses': expenses,
        'categories': categories,

        'pie_labels': pie_labels,
        'pie_totals': pie_totals,

        'line_labels': line_labels,
        'line_totals': line_totals,
    }

    # 💰 total
    total_gastos = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # 📊 promedio
    promedio_gastos = expenses.aggregate(avg=Avg('amount'))['avg'] or 0

    # 🏆 categoría top
    top_categoria = (
        expenses
        .values('expense_type__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )

    top_categoria_nombre = top_categoria['expense_type__name'] if top_categoria else "N/A"
    context.update({
        'total_gastos': total_gastos,
        'promedio_gastos': promedio_gastos,
        'top_categoria': top_categoria_nombre,
    })

    return render(request, 'expenses/dashboard.html', context)

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