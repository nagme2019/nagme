import redis
import pytz
import arrow

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField
from django.urls import reverse
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, primary_key=True)
    slug = models.SlugField(unique=True)
    subscribers = models.ManyToManyField('UserProfile')
    image = models.ImageField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        app_label = 'nagme_app'

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey('UserProfile')
    nag = models.ForeignKey('Nag')


class Subscribe(models.Model):
    user = models.ForeignKey('UserProfile')
    cat = models.ForeignKey('Category')


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    is_author = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'nagme_app'


class Nag(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='author', null=True)
    text = models.CharField(max_length=140, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        app_label = 'nagme_app'

