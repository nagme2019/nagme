from django.shortcuts import render, redirect, render_to_response
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


def base(request):
    return render(request, 'base.html')


def welcome(request):
    nag = Nag.objects.order_by('-likes')[0]
    category_list = Category.objects.all
    context_dict = {
        "nag_of_the_day": nag, "category_list": category_list}
    return render(request, 'nagme/welcome_page.html', context_dict)


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
def user_home(request):
    category_list = Category.objects.all
    nag = Nag.objects.order_by('-likes')[0]
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]

    context_dict = {
        "nag_of_the_day": nag,
        "categories": category_list,
        'userprofile': userprofile,
    }

    return render(request, 'nagme/user_home.html', context_dict)


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
        else:
            print(form.errors)

    return render(request, 'nagme/account.html',
                  {'userprofile': userprofile, 'user': user, 'form': form})


@login_required
def like(request, n):
    n.likes += 1
    return render(request, 'nagme/nags.html')


@login_required
def is_liked(request, text):
    nag = Nag.object.filter(text=text)[0]
    return Like.objects.filter(user=request.user, nag=nag).exists()


@login_required
def subscribe(request, cat):
    new_sub, created = Subscribe.objects.get_or_create(user=request.user, category=cat.name)
    if created:
        category.subscribers += 1


@login_required
def is_subbed(request, cat):
    return Subscribe.objects.filter(user=request.user, category=cat.name).exists()


@login_required
def add_nag(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = NagForm(request.POST)
        if form.is_valid():
            if cat:
                nag = form.save(commit=True)
                nag.category = cat
                nag.likes = 0
                nag.save()
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = NagForm()

    context_dict = {'form': form, 'category': cat}
    return render('nagme/add_nag.html', context_dict)


@login_required
def nags_likes(request):
    nag_list = Nag.objects.order_by('-likes')
    context_dict = {"nags": nag_list}

    return render(request, 'nagme/nags.html', context_dict)


@login_required
def nags_time(request):
    nag_list = Nag.objects.order_by('-created')
    context_dict = {"nags": nag_list}

    return render(request, 'nagme/nags.html', context_dict)


@login_required
def subscribed_categories(request):
    user = request.user
    category_list = Category.objects.filter(subscribers=user)
    context_dict = {"categories": category_list}

    return render(request, 'nagme/subscribed_categories.html', context_dict)


def send_email(subject, emails, content):
    send_mail(subject, content, 'nagmebot2019@gmail.com', emails)


def send_nags(request, category_name_slug):
    try:
        nag_cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        nag_cat = None
    print(category_name_slug)
    emails = []
    subscribers = Subscribe.objects.filter(cat=nag_cat)
    nag = Nag.objects.filter(category=nag_cat).order_by('-likes')[0]
    for s in subscribers:
        emails.append(s.user.email)
        send_text(s.user.name, s.user.phone_number, s.nag.text)
    if not emails:
        emails.append(request.user.email)
    print(emails)
    send_email('Nag', emails, nag.text)
    return category(request, category_name_slug)


def send_nags_text(request, category_name_slug):
    nag_cat = Category.objects.get(slug=category_name_slug)
    nag = Nag.objects.filter(category=nag_cat).order_by('-likes')[0]
    user = UserProfile.objects.filter(user=request.user)[0]
    number = user.phone_number
    print(number)
    send_text(number, nag.text)
    return category(request, category_name_slug)


# call sent_text with number you want to send to and content being what you want to send
def send_text(number, content):
    # should be private
    account_sid = ''
    auth_token = ''
    nagme_number = ''
    if not number:
        print("no")

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=content,
        from_=nagme_number,
        to=number
        )
    print(message.sid)


def support(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data.get("contact_name")
        email = form.cleaned_data.get("contact_email")
        message = form.cleaned_data.get("content")
        content = name + "\n" + email + "\n" + message
        print("message recieved")
        send_email('Support', ['nagmebot2019@gmail.com'], content)
        context = {'form': form}
        return render(request, 'nagme/support.html', context)
    else:
        return render(request, 'nagme/support.html', {'form': form})


@login_required
def categories(request):
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    return render(request, 'nagme/categories.html', context_dict)


@login_required
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

    return render(request, 'nagme/category_page.html', context_dict)
