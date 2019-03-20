import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nagme_project.settings')

import django

django.setup()
from nagme_app.models import Category, UserProfile, Nag, Reminder


def populate():
    hygiene_nags = [
        {"text": "Remember to wash behind your ears"},
        {"text": "You clean? Scrub up and feel better!"},
        {"text": "Take a shower, find your power!"},
        {"text": "Remember to brush your teeth today!"},
        {"text": "Do everyone around you a favour. Wash up!"},
        {"text": "Shower time! Cleanliness is next to Godliness"},
        {"text": "You deserve a shower, not too long though ;)"},
        {"text": "Remember, you only don’t want to get in until you don’t want to get out"},
        {"text": "Get the water running! Shower time!"},
        {"text": "Brush your teeth! Or at least the ones you want to keep"},
    ]

    wake_nags = [
        {"text": "Time to get up!"},
        {"text": "Hello! This is your wakeup call!"},
        {"text": "The day’s waiting for you, wake up!!!"},
        {"text": "Come on! Time to get up sleepyhead!"},
        {"text": "Nights over sunshine, up you get!!!"},
        {"text": "Time to face the day!!! Out of bed and make it neat"},
        {"text": "What are you doing still in bed? Get up!!!"},
        {"text": "Carpe Diem! That means seize the day"},
        {"text": "Struggling to get up? Countdown from 10, and get up before you’re finished. 3… 2… 1… Go!"},
        {"text": "Up Up Up! Let’s go! Let’s go!"},
    ]

    house_nags = [
        {"text": "Tidy your room"},
        {"text": "Do laundry"},
        {"text": "Wash the dishes", "subscriber": "Max"},
    ]

    work_nags = [
        {"text": "Do your assignment"},
    ]

    cats = {"Hygiene": {"nags": hygiene_nags, "image": "images/Cat_Hygiene"},
            "House": {"nags": house_nags, "image": "images/Cat_getout"},
            "Work": {"nags": work_nags, "image": "images/"},
            "Wake": {"nags": wake_nags, "image": "images/"},
            }

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for n in cat_data["nags"]:
            add_nag(c, n["text"])

    for c in Category.objects.all():
        for n in Nag.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(n)))


def add_nag(cat, text, likes=0):
    n = Nag.objects.get_or_create(category=cat, text=text)[0]
    n.likes = likes
    n.save()
    return n


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c


def add_user(name, phonenumber):
    u = UserProfile.objects.get_or_create(name=name, phonenumber=phonenumber)[0]
    u.save()
    return u


def add_reminder(name, time, text):
    r = Reminder.objects.get_or_create(name=name, time=time, text=text)[0]
    r.phonenumber = name.phonenumber
    r.save()
    return r


if __name__ == '__main__':
    print("Starting NagMe population script...")
    populate()
