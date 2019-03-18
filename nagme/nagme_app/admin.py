from django.contrib import admin
from nagme_app.models import Category, UserProfile, Nag, Reminder


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'top')


class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phonenumber', 'isauthor')


class NagAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'author', 'likes', 'created')


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Nag, NagAdmin)
admin.site.register(Reminder)
