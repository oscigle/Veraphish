from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import UserCreationForm


def register(request):

    ''' Register a given user. 

    Function disabled in URLS by default, since makes no sense
    in most environments. '''

    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                do_login(request, user)
                return redirect('/SETA_gophish')
    return render(request, "users/register.html", {'form': form})


def login(request):

    ''' Log in a given user. 

    Standard form user/pass. '''

    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                return redirect(request.GET.get('next','/SETA_gophish'))
    return render(request, "users/login.html", {'form': form})


def logout(request):

    ''' Log out a given user. 

    Redirect to main page afterwards. '''

    do_logout(request)
    return redirect('/SETA_gophish')
