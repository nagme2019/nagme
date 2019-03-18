from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from nagme_app.models import Category, Nag, Reminder
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.contrib.messages.views import SuccessMessageMixin


def base(request):

    return render(request, 'base.html')


def welcome(request):

    return render(request, 'nagme/welcome_page.html')


# added an underscore temporarily because name conflict with import at top,
    # need to fix name of this view everywhere later
def log_in(request):
    #need to change this so it stops giving the weird error from inbuilt login function
    #who is building forms?
    context_dict = {}

    return render(request, 'nagme/log_in.html', context_dict)


def registration(request):
    #who is making forms?
    context_dict = {}

    return render(request, 'nagme/registration.html', context_dict)


def userhome(request):
    #change to only allow if user is logged in,
    #otherwise redirect to login page
    #need to figure out how to display categories

    context_dict = {
        "firstname":"FirstName",
        "username": "username",
        "days_using": 184,
        "nag_of_the_day" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras id maximus ante, et vehicula magna. Fusce vel rhoncus dui. \n Curabitur lacinia mattis arcu in sollicitudin."
        }

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


# ##############################################################################
# The dictionaries below temporary


topbarBtns = {
    "signup": {"label": "Sign Up", "link": 'signup', "icon": "fas fa-user-plus"},
    "login": {"label": "Log In", "link": 'login', "icon": "fas fa-sign-in-alt"},
    "logout": {"label": "Log Out", "link": 'logout', "icon": "fas fa-sign-out-alt"},
    "contact": {"label": "Contact Us", "link": 'contact', "icon": "fas fa-question"},
    "welcome": {"label": "Back to Welcome Page", "link": 'welcome', "icon": "fas fa-home"},
    "empty": {"label": "", "link": '#', "icon": ""}
}


'''
    bell -slash bells  ,  badge -check ,  ban
    calendar -alt -check -day - week
            -edit -exclamation -minus -plus - star -times(looks like x)
    minus -circle -square -hexagon -octagon
    comments , comment -slash -alt -alt-slash  ,  sms , quote-left -right
    mobile -alt
    lock -open -alt -open-alt
    exclamation -square -triangle
    info -square -circle
    eye -slash
    bullhorn bullseye certificate
    chart-area -bar -line -pie
    tag tags
    thumbtack
    tasks
    smile frown meh
    clock , hourglass -end -start -half
'''
