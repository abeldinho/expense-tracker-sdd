from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, "Cuenta creada correctamente")
            return redirect("expenses:ingresar_expense")
        messages.error(request, "Error en el formulario")
    else:
        form = SignUpForm()

    return render(request, "auth_users/signup.html", {"form": form})
