from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from nagme_app.models import Category, Nag, Like, Subscribe, UserProfile
from django.conf import settings
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
                login(request, user)
                return HttpResponseRedirect(reverse('user_home'))
            else:
                return HttpResponse("Your Nag.Me account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
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
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'nagme/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('welcome'))


@login_required
def user_home(request):
    # change to only allow if user is logged in,
    # otherwise redirect to login page

    category_list = Category.objects.all
    nag = Nag.objects.order_by('-likes')[0]
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]

    context_dict = {
        "firstname": "FirstName",
        "username": "username",
        "days_using": 184,
        "nag_of_the_day": nag,
        "categories": category_list,
        'userprofile': userprofile,
    }

    return render(request, 'nagme/user_home.html', context_dict)


# change so user can change email/first name/etc etc
@login_required
def account(request):
    user = request.user
    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    form = UserProfileForm(
        {'phone_number': userprofile.phone_number,
         'picture': userprofile.picture})

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=userprofile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('account')
        else: print(form.errors)

    return render(request, 'nagme/account.html',
                  {'userprofile': userprofile, 'user': user, 'form': form})


@login_required
def account_password(request):
    context_dict = {}

    return render(request, 'nagme/account_password.html', context_dict)


@login_required
def like(request, user, nag):
    new_like,created = Like.objects.get_or_create(user=user.user, nag_id=nag.id)
    if created:
        nag.likes += 1


@login_required
def is_liked(request, user, nag):
    return Like.objects.filter(user=user.user, nag=nag.id).exists()


@login_required
def subscribe(request, user, category):
    new_sub, created = Subscribe.objects.get_or_create(user=user.user, category=category.name)
    if created:
        category.subscribers += 1

@login_required
def is_subbed(request, user, category):
    return Subscribe.objects.filter(user=user.user, cat=category.name).exists()


def is_subbed(request, username, category):
    return Subscribe.objects.filter(user=username, cat=category).exists()
    if not created:
        return False
    else:
        return True


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





def nags_likes(request):
    nag_list = Nag.objects.order_by('-likes')
    context_dict = {"nags": nag_list}

    return render(request, 'nagme/nags.html', context_dict)


def nags_time(request):
    nag_list = Nag.objects.order_by('-created')
    context_dict = {"nags": nag_list}

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


# emails = emails to send to
def send_email(subject, emails, content):
    send_mail(subject, content, 'nagmebot2019@gmail.com', emails)


def send_nags(request,category_name_slug):
    emails=[]
    nag_cat = Category.objects.get(slug=category_name_slug)
    subscribers=Subscribe.objects.filter(cat=nag_cat)
    for s in subscribers:
        emails.add(s.user.email)
    print(emails)
    nag= Nag.objects.filter(category=nag_cat).order_by('-likes')[0]
    send_mail('Nag',nag.text,'nagmebot2019@gmail.com',emails)

    return category(request, category_name_slug)

# call sent_text with number you want to send to and content being what you want to send
def send_text(name, number, content):
    account_sid = 'ACf46f7868cc321426fc41dbbe0ea4676e'
    auth_token = 'f091327b9ce1bb5900b28edc8bb416b3'
    nagme_number = '+447480534396'
    test = '+447365140632'
    if (not number):
        print("no")

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=content,
        from_=nagme_number,
        to=test
    )
    print(message.sid)


def support(request):
    #if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name= form.cleaned_data.get("contact_name")
            email= form.cleaned_data.get("contact_email")
            message=form.cleaned_data.get("content")
            content= name+"\n"+email+"\n"+message
            print ("message recieved")
            send_email('Support',['nagmebot2019@gmail.com'],content)
            #send_nags("Wake",['oliver.warke@gmail.com'])
            context= {'form': form}
            return render(request, 'nagme/support.html', context)
        else:
            context= {'form': form}
            return render(request, 'nagme/support.html', {'form': form})
    #else:
     #   return render(request, 'nagme/support.html', {})



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
        context_dict['subbed'] = Subscribe.objects.filter(user=request.user.user)
    except Category.DoesNotExist:
        context_dict['nag'] = None
        context_dict['category'] = None

    return render(request, 'nagme/category_page.html', context_dict)


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
