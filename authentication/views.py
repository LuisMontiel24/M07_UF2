from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Usuario
from django.contrib.auth import login as auth_login, logout as auth_logout


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = Usuario.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                return redirect('home')
            except Usuario.DoesNotExist:
                messages.error(request, 'Credenciales incorrectas')
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})


def home_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    user = Usuario.objects.get(id=user_id)
    return render(request, 'authentication/home.html', {'user': user})


def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')