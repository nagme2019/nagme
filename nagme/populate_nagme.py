import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nagme_project.settings')

import django

django.setup()
from nagme_app.models import Category, User, Nag


def populate():
    hygiene_nags = [
        {"text": "Remember to wash behind your ears", "likes": 12},
        {"text": "You clean? Scrub up and feel better!", "likes": 14},
        {"text": "Take a shower, find your power!", "likes": 16},
        {"text": "Remember to brush your teeth today!", "likes": 90},
        {"text": "Do everyone around you a favour. Wash up!", "likes": 0},
        {"text": "Shower time! Cleanliness is next to Godliness", "likes": 12},
        {"text": "You deserve a shower, not too long though ;)", "likes": 12},
        {"text": "Remember, you only don’t want to get in until you don’t want to get out", "likes": 0},
        {"text": "Get the water running! Shower time!", "likes": 90},
        {"text": "Brush your teeth! Or at least the ones you want to keep", "likes": 12},
    ]

    wake_nags = [
        {"text": "Time to get up!", "likes": 0},
        {"text": "Hello! This is your wakeup call!", "likes": 90},
        {"text": "The day’s waiting for you, wake up!!!", "likes": 16},
        {"text": "Come on! Time to get up sleepyhead!", "likes": 12},
        {"text": "Nights over sunshine, up you get!!!", "likes": 90},
        {"text": "Time to face the day!!! Out of bed and make it neat", "likes": 16},
        {"text": "What are you doing still in bed? Get up!!!", "likes": 12},
        {"text": "Carpe Diem! That means seize the day", "likes": 90},
        {"text": "Struggling to get up? Countdown from 10, and get up before you’re finished. 3… 2… 1… Go!", "likes": 14},
        {"text": "Up Up Up! Let’s go! Let’s go!", "likes": 16},
    ]

    time_nags = [
        {"text": "Don't be late! Get going nice and early", "likes": 16},
        {"text": "Leaving in plenty of time gives you lots of time to relax once you’re there", "likes": 13},
        {"text": "“Better 3 hours too soon than 1 minute too late” - Shakespeare", "likes": 12},
        {"text": "Don’t even think about leaving at the last minute. Go now so you don’t rush!", "likes": 11},
        {"text": "Get on your way! Out Out Out!", "likes": 90},
        {"text": "Get that behind out the door buster", "likes": 16},
        {"text": "Go Go Go! The day awaits! Be strong!", "likes": 10},
        {"text": "Get up, get out!", "likes": 90},
    ]

    studying_nags = [
        {"text": "If you can read this you’re not working. Get to it!", "likes": 11},
        {"text": "Putting your phone away will help eliminate distractions", "likes": 10},
        {"text": "Put that phone down for 25 minutes and get yourself ahead", "likes": 12},
        {"text": "Work's got to get done eventually, might as well be now", "likes": 17},
        {"text": "The best time to plant a tree was 20 years ago. The second best time is right now", "likes": 10},
        {"text": "Dig Deep! Put this away, get cracking!", "likes": 14},
        {"text": "“Work Work Work” - Rihanna", "likes": 12},
        {"text": "Work hard!", "likes": 10},
        {"text": "Checking in! Hope you’re working hard!", "likes": 24},
        {"text": "Crack on with that work honey", "likes": 12}
    ]

    money_nags = [
        {"text": "A penny saved is a penny earned", "likes": 16},
        {"text": "A fool and their money are soon parted", "likes": 13},
        {"text": "Stop, think, Save", "likes": 11},
        {"text": "Make sure you look over your budget today!", "likes": 19},
        {"text": "Think before you buy: you could probably use that money later", "likes": 11},
        {"text": "Be sensible with your cash today", "likes": 10},
        {"text": "Don’t splash. Wait a day before you pay", "likes": 15},
        {"text": "Best not to buy more than you need", "likes": 0},
        {"text": "Take it easy tiger. Don’t pour too much cash down your neck", "likes": 12},
        {"text": "Save the pennies and the pounds soon follow", "likes": 11}
    ]

    sleep_nags = [
        {"text": "Early to bed, early to rise, makes a man healthy wealthy and wise", "likes": 100},
        {"text": "Off to bed. Good night. Tomorrow's a new day", "likes": 12},
        {"text": "You’ll regret staying up late in the morning", "likes": 1},
        {"text": "Get a wee early night. Will do you good!", "likes": 16},
        {"text": "Time to close your eyes and count some sheep!", "likes": 11},
        {"text": "You don’t want to get into bed, but tomorrow you won’t want to get out!", "likes": 14},
        {"text": "Time to wind down. Good night", "likes": 162},
        {"text": "Away to bed now. Sleep well!", "likes": 16},
        {"text": "The sooner you get to sleep the sooner you’ll be dreaming", "likes": 12},
        {"text": "Come on! Don’t have another late night!", "likes": 16}
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
            add_nag(c, n["text"], n["likes"]),

    for c in Category.objects.all():
        for n in Nag.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(n)))


# Add Categories
def add_cat(name, image):
    c = Category.objects.get_or_create(name=name, image=image)[0]
    c.save()
    return c


# Add Nags
def add_nag(category, nag, likes):
    n = Nag.objects.get_or_create(category=category, text=nag)[0]
    n.likes = likes
    n.save()
    return n


if __name__ == '__main__':
    print("Starting NagMe population script...")
    populate()
