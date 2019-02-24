from django.contrib import admin
from nagme.models import Category, User, Nag

# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Nag)