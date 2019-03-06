from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from nagme.models import Reminder
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from nagme.models import Category, Nag


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
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    return render(request, 'nagme/categories.html', context_dict)


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

    return render(request, 'nagme/category.html', context_dict)


class ReminderCreateView(SuccessMessageMixin, CreateView):
    model = Reminder
    fields = ['name', 'phonenumber', 'time', 'text']
    success_message = 'Reminder successfully created'
