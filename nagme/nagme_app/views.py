from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from nagme_app.models import Category, Nag
from django.contrib.auth.models import User
from twilio.rest import Client
from .forms import ContactForm, UserForm, UserProfileForm, NagForm
from nagme_project.settings import TWILIO_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


def base(request):
    return render(request, 'base.html')


def welcome(request):
    nag = Nag.objects.order_by('-likes')[0]

    context_dict = {
        "nag_of_the_day": nag}

    return render(request, 'nagme/welcome_page.html', context_dict)


# added an underscore temporarily because name conflict with import at top,
# need to fix name of this view everywhere later
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                log_in(request, user)
                return HttpResponseRedirect('user_home')
            else:
                return HttpResponse("Your Nag.Me account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'nagme/log_in.html', {})


def registration(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print (user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'nagme/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_home(request):
    # change to only allow if user is logged in,
    # otherwise redirect to login page

    category_list = Category.objects.all
    nag = Nag.objects.order_by('-likes')[0]

    context_dict = {
        "firstname": "FirstName",
        "username": "username",
        "days_using": 184,
        "nag_of_the_day": nag,
        "categories": category_list,
    }

    return render(request, 'nagme/user_home.html', context_dict)


@login_required
def account(request):
    # remember to make sure only to allow is user is logged in later
    # TODO add firstname, lastname, email to profile?
    user = request.user
    context_dict = {
        "username": user.user,
        "phone_number": user.phone_number,
        "password": "********",
    }
    return render(request, 'nagme/manage_account.html', context_dict)


@login_required
def account_details(request):
    context_dict = {}

    return render(request, 'nagme/account_details.html', context_dict)


@login_required
def account_password(request):
    context_dict = {}

    return render(request, 'nagme/account_password.html', context_dict)


#def like(request, nag_id):
    #TODO


#def subscribe(request, cat):
    #TODO


# make sure it can't be accessed unless the person is an author
# currently set up so author can add nag from chosen category page, assume we want to
# make it possible for them to choose the category from a drop down list on the add
# nag page
@login_required
def add_nag(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    form = NagForm()
    if request.method == 'POST':
        form = NagForm(request.POST)
        if form.is_valid():
            if cat:
                nag = form.save(commit=False)
                nag.category = cat
                nag.likes = 0
                nag.save()
                return cat(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': cat}
    return render(request, 'nagme/add_nag.html', context_dict)


#call sent_text with number you want to send to and content being what you want to send
def send_text(name, number, content):
    account_sid = 'ACf46f7868cc321426fc41dbbe0ea4676e'
    auth_token = 'f091327b9ce1bb5900b28edc8bb416b3'
    nagme_number='+447480534396'
    test='+447365140632'
    if(not number):
        print("no")

    client= Client(account_sid,auth_token)

    message=client.messages \
             .create(
                 body=content,
                 from_=nagme_number,
                 to=test
             )
    print(message.sid)


def nags_likes(request):
    nag_list = Nag.objects.order_by('-likes')
    context_dict = {"nags": nag_list, "nag_page_title": "Popular Nags"}

    return render(request, 'nagme/nags.html', context_dict)


def nags_time(request):
    nag_list = Nag.objects.order_by('-created')
    context_dict = {"nags": nag_list, "nag_page_title": "Recent Nags"}

    return render(request, 'nagme/nags.html', context_dict)


# def subscribed_nags(request):
#     user = request.user
#     nag_list = Nag.objects.filter(subscriber=user)
#     context_dict = {"nags": nag_list}
#
#     return render(request, 'nagme/subscribed_nags.html', context_dict)


@login_required
def subscribed_categories(request):
    user = request.user
    category_list = Category.objects.filter(subscribers=user)
    context_dict = {"categories": category_list}

    return render(request, 'nagme/subscribed_categories.html', context_dict)


def support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name= form.cleaned_data.get("contact_name")
            number= form.cleaned_data.get("contact_number")
            content=form.cleaned_data.get("content")
            print(number)
            print ("message recieved")
            send_text(name,number,content)
            context= {'form': form}
            return render(request, 'nagme/support.html', context)
        else:
            context= {'form': form}
            return render(request, 'nagme/support.html', {'form': form})
    else:
        return render(request, 'nagme/support.html', {})


def categories(request):
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    return render(request, 'nagme/categories.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}

    try:
        cat = Category.objects.get(slug=category_name_slug)
        nag = Nag.objects.filter(category=cat)
        context_dict['nags'] = nag
        context_dict['category'] = cat
    except Category.DoesNotExist:
        context_dict['nag'] = None
        context_dict['category'] = None


# ##############################################################################
# The dictionaries below temporary


topbarBtns = {
    "signup": {"label": "Sign Up", "link": 'signup', "icon": "fas fa-user-plus"},
    "log_in": {"label": "Log In", "link": 'log_in', "icon": "fas fa-sign-in-alt"},
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
