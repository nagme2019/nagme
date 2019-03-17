from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from _nagme.models import Category, Nag


def base(request):
    context_dict = {}

    return render(request, 'base.html', context=context_dict)


def welcome(request):
    context_dict = {}

    return render(request, '_nagme/welcome_page.html', context_dict)


def login(request):
    context_dict = {}

    return render(request, '_nagme/login.html', context_dict)


def registration(request):
    context_dict = {}

    return render(request, '_nagme/registration.html', context_dict)


def userhome(request):
    context_dict = {}

    return render(request, '_nagme/userhome.html', context_dict)


def account(request):
    context_dict = {}

    return render(request, '_nagme/account.html', context_dict)


def account_details(request):
    context_dict = {}

    return render(request, '_nagme/account_details.html', context_dict)


def account_password(request):
    context_dict = {}

    return render(request, '_nagme/account_password.html', context_dict)


def addnag(request):
    context_dict = {}

    return render(request, '_nagme/addnag.html', context_dict)


def support(request):
    context_dict = {}

    return render(request, '_nagme/support.html', context_dict)


def categories(request):
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    return render(request, '_nagme/categories.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}

    try:
        cat = Category.objects.get(slug=category_name_slug)
        nags = Nag.objects.filter(category=cat)
        context_dict['nags'] = nags
        context_dict['category'] = cat
    except Category.DoesNotExist:
        context_dict['nag'] = None
        context_dict['category'] = None

