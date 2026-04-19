from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth_users/login.html',next_page='expenses:ingresar_expense'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='auth_users:login'),name='logout'),
    path('signup/', views.signup_view,name='register'),
    ]