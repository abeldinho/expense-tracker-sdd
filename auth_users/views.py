from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm

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

def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('expenses:registrar_expense')
        else:
            error = "Usuario o contraseña incorrectos"

    return render(request, 'auth_users/login.html', {
        'error': error
    })