import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nagme_project.settings')

import django

django.setup()
from nagme_app.models import Category, User, Nag


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

    time_nags = [
        {"text": "Don't be late! Get going nice and early"},
        {"text": "Leaving in plenty of time gives you lots of time to relax once you’re there"},
        {"text": "“Better 3 hours too soon than 1 minute too late” - Shakespeare"},
        {"text": "Don’t even think about leaving at the last minute. Go now so you don’t rush!"},
        {"text": "Get on your way! Out Out Out!"},
        {"text": "Get that behind out the door buster"},
        {"text": "Go Go Go! The day awaits! Be strong!"},
        {"text": "Get up, get out!"},
    ]

    studying_nags = [
        {"text": "If you can read this you’re not working. Get to it!"},
        {"text": "Putting your phone away will help eliminate distractions"},
        {"text": "Put that phone down for 25 minutes and get yourself ahead"},
        {"text": "Work's got to get done eventually, might as well be now"},
        {"text": "The best time to plant a tree was 20 years ago. The second best time is right now"},
        {"text": "Dig Deep! Put this away, get cracking!"},
        {"text": "“Work Work Work” - Rihanna"},
        {"text": "Work hard!"},
        {"text": "Checking in! Hope you’re working hard!"},
        {"text": "Crack on with that work honey"}
    ]

    money_nags = [
        {"text": "A penny saved is a penny earned"},
        {"text": "A fool and their money are soon parted"},
        {"text": "Stop, think, Save"},
        {"text": "Make sure you look over your budget today!"},
        {"text": "Think before you buy: you could probably use that money later"},
        {"text": "Be sensible with your cash today"},
        {"text": "Don’t splash. Wait a day before you pay"},
        {"text": "Best not to buy more than you need"},
        {"text": "Take it easy tiger. Don’t pour too much cash down your neck"},
        {"text": "Save the pennies and the pounds soon follow"}
    ]

    sleep_nags = [
        {"text": "Early to bed, early to rise, makes a man healthy wealthy and wise"},
        {"text": "Off to bed. Good night. Tomorrow's a new day"},
        {"text": "You’ll regret staying up late in the morning"},
        {"text": "Get a wee early night. Will do you good!"},
        {"text": "Time to close your eyes and count some sheep!"},
        {"text": "You don’t want to get into bed, but tomorrow you won’t want to get out!"},
        {"text": "Time to wind down. Good night"},
        {"text": "Away to bed now. Sleep well!"},
        {"text": "The sooner you get to sleep the sooner you’ll be dreaming"},
        {"text": "Come on! Don’t have another late night!"}
    ]

    cats = {"Hygiene": {"nags": hygiene_nags, "image": "/images/Cat_Hygiene.png"},
            "Wake": {"nags": wake_nags, "image": "/images/Cat_WakeUp.png"},
            "Get out": {"nags": time_nags, "image": "/images/Cat_getout.png"},
            "Studying": {"nags": studying_nags, "image": "/images/Cat_Study.png"},
            "Money": {"nags": money_nags, "image": "/images/Cat_Money.png"},
            "Sleep": {"nags": sleep_nags, "image": "/images/Cat_sleep.png"}
            }

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['image'])
        for n in cat_data["nags"]:
            add_nag(c, n["text"])

    for c in Category.objects.all():
        for n in Nag.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(n)))


# Add Categories
def add_cat(name, image):
    c = Category.objects.get_or_create(name=name, image=image)[0]
    c.save()
    return c


# Add Nags
def add_nag(category, nag, likes=0):
    n = Nag.objects.get_or_create(category=category, text=nag)[0]
    n.likes = likes
    n.save()
    return n


if __name__ == '__main__':
    print("Starting NagMe population script...")
    populate()
