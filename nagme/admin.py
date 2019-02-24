from django.contrib import admin
from nagme.models import Category, UserProfile, Nag


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
admin.site.register(Nag)
