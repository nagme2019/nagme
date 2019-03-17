from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from _nagme.models import Category, Nag, Reminder
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.contrib.messages.views import SuccessMessageMixin


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


class ReminderCreateView(SuccessMessageMixin, CreateView):
    model = Reminder
    fields = ['name', 'phonenumber', 'time', 'time_zone']
    success_message = 'Reminder successfully created.'


class ReminderListView(ListView):
    """Shows users a list of appointments"""

    model = Reminder


class ReminderDetailView(DetailView):
    """Shows users a single appointment"""

    model = Reminder


class ReminderUpdateView(SuccessMessageMixin, UpdateView):
    """Powers a form to edit existing appointments"""

    model = Reminder
    fields = ['name', 'phonenumber', 'time', 'time_zone']
    success_message = 'Reminder successfully updated.'


class ReminderDeleteView(DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Reminder
    success_url = reverse_lazy('list_appointments')