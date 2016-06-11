from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect

from . forms import UserLoginForm, UserRegisterForm


def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return HttpResponseRedirect(reverse('posts:list'))

    return render(request, 'account_form.html', {'form': form, 'title': title})


def register_view(request):
    next = request.GET.get('next')
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        messages.success(request, "New User registered")
        if next:
            return redirect(next)
        return HttpResponseRedirect(reverse('login'))

    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'account_form.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
