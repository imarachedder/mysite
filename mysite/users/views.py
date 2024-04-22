from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        else:
            user = User.objects.create(username=username, password=password)
            user.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username, password=password).first()
        # user = User.objects.filter(username=username).first()

        if user:
            # Войти в систему, например, установить сеанс
            return redirect('home')  # Перенаправить на вашу домашнюю страницу
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # user = authenticate(username=username, password=password)
        user = User.objects.filter(username=username, password=password).first()
        print(user)
        if user is not None:
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'account_locked.html')
        else:
            return render(request, 'invalid_credentials.html')
    else:
        return render(request, 'login.html')


