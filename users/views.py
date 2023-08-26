from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm


def loginUser(request):
    context = {
        'page_title': 'LOGIN',
    }
    user = None
    if request.method == "POST":

        username_login = request.POST['username']
        password_login = request.POST['password']

        user = authenticate(request, username=username_login,
                            password=password_login)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')
            return redirect('login')

    return render(request, 'users/login.html', context)


def logoutUser(request):

    if request.method == "POST":
        if request.POST["logout"]:
            logout(request)

        return redirect('login')

    return render(request, 'users/logout.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})