from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, primary_key=True)
    top = models.ForeignKey('Nag', on_delete=models.SET_NULL, related_name='top', null=True)  # change the on_delete to the next most liked nag
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        app_label = '_nagme'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phonenumber = PhoneNumberField(null=False, blank=False, unique=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    isauthor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = '_nagme'


class Nag(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='author', null=True)
    text = models.CharField(max_length=140, unique=True)
    likes = models.PositiveIntegerField(default=0)
    subscriber = models.ManyToManyField(User, related_name='subscribe')
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        app_label = '_nagme'


class Reminder(models.Model):
    name = models.ManyToManyField('UserProfile', related_name='subscriber')
    phonenumber = models.ManyToManyField('UserProfile', related_name='phonenumber')  # this should be automatically set to the user's number
    time = models.DateTimeField()
    text = models.ForeignKey('Nag')

    def __str__(self):
        return 'Reminder #{0} - {1}'.format(self.pk, self.text)

    class Meta:
        app_label = '_nagme'
