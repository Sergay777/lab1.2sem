from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
 # Создаем нового пользователя
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            user = authenticate(username=cd['username'], password=cd['password'])
            login(request, user)
 # Можно сразу добавить группу/роль, но пока пропустим
 # После создания пользователя, можно залогинить его или перенаправить на страницу входа
            return redirect('login') # перенаправим на страницу входа (реализуем позже)
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
# Create your views here.
