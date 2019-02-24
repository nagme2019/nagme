from django.db import models
from django.template.defaultfilters import slugify
#from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, primary_key=True)
    top = models.ForeignKey('Nag', on_delete=models.SET_NULL, related_name='top', null=True) # change the on_delete
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=16, unique=True, primary_key=True)
    forename = models.CharField(max_length=16)
    surname = models.CharField(max_length=16)
    email = models.EmailField(max_length=254)
    #phonenumber = PhoneNumberField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=16)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    isauthor = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Nag(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE) # change this
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author', null=True)
    text = models.CharField(max_length=140, unique=True)
    likes = models.PositiveIntegerField(default=0)
    subscriber = models.ManyToManyField(User, related_name='subscribe', null=True)

    def __str__(self):
        return self.text  # is this right?

