from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def welcome(request):
    context_dict = {}

    return render(request, 'nagme/welcome.html', context_dict)


def login(request):
    context_dict = {}

    return render(request, 'nagme/login.html', context_dict)


def registration(request):
    context_dict = {}

    return render(request, 'nagme/registration.html', context_dict)


def userhome(request):
    context_dict = {}

    return render(request, 'nagme/userhome.html', context_dict)


def account(request):
    context_dict = {}

    return render(request, 'nagme/account.html', context_dict)


def account_details(request):
    context_dict = {}

    return render(request, 'nagme/account_details.html', context_dict)


def account_password(request):
    context_dict = {}

    return render(request, 'nagme/account_password.html', context_dict)


def addnag(request):
    context_dict = {}

    return render(request, 'nagme/addnag.html', context_dict)


def support(request):
    context_dict = {}

    return render(request, 'nagme/support.html', context_dict)


def categories(request):
    context_dict = {}

    return render(request, 'nagme/categories.html', context_dict)


def category(request):
    context_dict = {}

    return render(request, 'nagme/category.html', context_dict)

