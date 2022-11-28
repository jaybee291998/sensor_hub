from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

from .forms import UserLoginForm

# Create your views here.
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(email = email, password = password)
        login(request, user)
        return redirect('home')
    context = {
        'form':form
    }
    return render(request, 'account/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    context = {

    }
    return render(request, 'app.html', context)

