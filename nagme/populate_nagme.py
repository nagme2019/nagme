import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nagme.settings')

import django
django.setup()
from nagme.models import Category, User, Nag


def populate():
	nags ={"Wake Up": [
			["Time to get up!", "mombot"],
			["Hello! This is your wakeup call!", "mombot"],
			["The day’s waiting for you, wake up!!!", "mombot"],
			["Come on! Time to get up sleepyhead!", "mombot"],
			["Nights over sunshine, up you get!!!", "mombot"],
			["Time to face the day!!! Out of bed and make it neat", "mombot"],
			["What are you doing still in bed? Get up!!!", "mombot"],
			["Carpe Diem! That means seize the day", "mombot"],
			["Struggling to get up? Countdown from 10, and get up before you’re finished. 3… 2… 1… Go!", "mombot"],
			["Up Up Up! Let’s go! Let’s go!", "mombot"]]
		"Hygiene" : [
			["Remember to wash behind your ears", "mombot"],
			["You clean? Scrub up and feel better!", "mombot"],
			["Take a shower, find your power!", "mombot"],
			["Remember to brush your teeth today!", "mombot"],
			["Do everyone around you a favour. Wash up!", "mombot"],
			["Shower time! Cleanliness is next to Godliness", "mombot"],
			["You deserve a shower, not to long though ;)", "mombot"],
			["Remember, you only don’t want to get in until you don’t want to get out", "mombot"],
			["Get the water running! Shower time!", "mombot"],
			["Brush your teeth! Or at least the ones you want to keep", "mombot"]],
		"Being on Time": [
			["Don’t be late! Get going nice and early", "mombot"],
			["Leaving in plenty of time gives you lots of time to relax once you’re there", "mombot"],
			["\“Better 3 hours too soon than 1 minute too late\” - Shakespeare", "mombot"],
			["Don’t even think about leaving at the last minute. Go now so you don’t rush!", "mombot"],
			["Get on your way! Out Out Out!", "mombot"],
			["Get that behind out the door buster", "mombot"],
			["Go Go Go! The day awakes! Be strong!", "mombot"],
			["Get up, get out!", "mombot"]],
		"Studying": [
        	["If you can read this you’re not working. Get to it!", "mombot"],
			["Putting your phone away will help eliminate distractions", "mombot"],
			["Put that phone down for 25 minutes and get yourself ahead", "mombot"],
			["Works got to get done eventually, might as well be now", "mombot"],
			["The best time to plant a tree was 20 years ago. The second best time is right now", "mombot"],
			["Dig Deep! Put this away, get cracking!", "mombot"],
			["“Work Work Work” -Rihanna", "mombot"],
			["Work hard!", "mombot"],
			["Checking in! Hope you’re working hard!", "mombot"],
			["Crack on with that work honey", "mombot"]],
		"Money": [
			["A penny saved is a penny earned", "mombot"],
			["A fool and their money are soon parted", "mombot"],
			["Stop, think, Save", "mombot"],
			["Make sure you look over your budget today!", "mombot"],
			["Think before you buy: you could probably use that money later", "mombot"],
			["Be sensible with your cash today", "mombot"],
			["Don’t splash. Wait a day before you pay", "mombot"],
			["Best not to buy more than you need", "mombot"],
			["Take it easy tiger. Don’t pour too much cash down your neck", "mombot"],
			["Save the pennies and the pounds soon follow", "mombot"]],
		"Sleep": [
			["Early to bed, early to rise, makes a man healthy wealthy and wise", "mombot"],
			["Off to bed. Good night. Tomorrow's a new day", "mombot"],
			["You’ll regret staying up late in the morning", "mombot"],
			["Get a wee early night. Will do you good!", "mombot"],
			["Time to close your eyes and count some sheep!", "mombot"],
			["You don’t want to get into bed, but tomorrow you won’t want to get out!", "mombot"],
			["Time to wind down. Good night", "mombot"],
			["Away to bed now. Sleep well!", "mombot"],
			["The sooner you get to sleep the sooner you’ll be dreaming", "mombot"],
			["Come on! Don’t have another late night!", "mombot"]]}


	for c, c_data in nags:
		add_cat(c)
		for elt in cat_data:
			add_nag(c, elt[0], elt[1])

	for u,u_data in users:



#Add Categories
def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

#Add Nags
def add_nag(category, nag, author):
	n = nag.objects.get_or_create(
	category=category,
	text = nag

	)
	n.save()
	return n



if __name__ == '__main__':
    print("Starting NagMe population script...")
    populate()
