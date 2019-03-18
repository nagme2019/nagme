import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nagme.settings')

import django
django.setup()
from nagme.models import Category, User, Nag


def populate():
	wakeup_nags = [
		"Time to get up!",
		"Hello! This is your wakeup call!",
		"The day’s waiting for you, wake up!!!",
		"Come on! Time to get up sleepyhead!",
		"Nights over sunshine, up you get!!!",
		"Time to face the day!!! Out of bed and make it neat",
		"What are you doing still in bed? Get up!!!",
		"Carpe Diem! That means seize the day",
		"Struggling to get up? Countdown from 10, and get up before you’re finished. 3… 2… 1… Go!",
		"Up Up Up! Let’s go! Let’s go!"
	]

   hygiene_nags = [
        "Remember to wash behind your ears",
		"You clean? Scrub up and feel better!",
		"Take a shower, find your power!",
		"Remember to brush your teeth today!",
		"Do everyone around you a favour. Wash up!",
		"Shower time! Cleanliness is next to Godliness",
		"You deserve a shower, not to long though ;)",
		"Remember, you only don’t want to get in until you don’t want to get out",
		"Get the water running! Shower time!",
		"Brush your teeth! Or at least the ones you want to keep"
    ]

	being_on_time_nags = [
        "Don’t be late! Get going nice and early",
		"Leaving in plenty of time gives you lots of time to relax once you’re there",
		"\“Better 3 hours too soon than 1 minute too late\” - Shakespeare",
		"Don’t even think about leaving at the last minute. Go now so you don’t rush!",
		"Get on your way! Out Out Out!",
		"Get that behind out the door buster",
		"Go Go Go! The day awakes! Be strong!",
		"Get up, get out!"
    ]

    study_nags = [
        "If you can read this you’re not working. Get to it!",
		"Putting your phone away will help eliminate distractions",
		"Put that phone down for 25 minutes and get yourself ahead",
		"Works got to get done eventually, might as well be now",
		"The best time to plant a tree was 20 years ago. The second best time is right now",
		"Dig Deep! Put this away, get cracking!",
		"“Work Work Work” -Rihanna",
		"Work hard!",
		"Checking in! Hope you’re working hard!",
		"Crack on with that work honey"
    ]

	money_nags = [
		"A penny saved is a penny earned",
		"A fool and their money are soon parted",
		"Stop, think, Save",
		"Make sure you look over your budget today!",
		"Think before you buy: you could probably use that money later",
		"Be sensible with your cash today",
		"Don’t splash. Wait a day before you pay",
		"Best not to buy more than you need",
		"Take it easy tiger. Don’t pour too much cash down your neck",
		"Save the pennies and the pounds soon follow"
	]

	bedtime_nags = [
		"Early to bed, early to rise, makes a man healthy wealthy and wise",
		"Off to bed. Good night. Tomorrow's a new day",
		"You’ll regret staying up late in the morning",
		"Get a wee early night. Will do you good!",
		"Time to close your eyes and count some sheep!",
		"You don’t want to get into bed, but tomorrow you won’t want to get out!",
		"Time to wind down. Good night",
		"Away to bed now. Sleep well!",
		"The sooner you get to sleep the sooner you’ll be dreaming",
		"Come on! Don’t have another late night!"
	]

    cats = {"Wake Up": {"nags":wakeup_nags},
			"Hygiene": {"nags": hygiene_nags}
            "Being on time": {"nags": being_on_time_nags},
            "study": {"nags":study_nags},
			"Money": {"nags": money_nags}
			"Bedtime": {"nags": bedtime_nags}
            }

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for n in cat_data:
            add_nag(c, n)

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


if __name__ == '__main__':
    print("Starting NagMe population script...")
    populate()
