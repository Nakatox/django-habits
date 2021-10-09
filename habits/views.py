from django.shortcuts import render, redirect
from django import forms

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm



# Create your views here.

def index(request):
    return render(request, "habits/index.html")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})