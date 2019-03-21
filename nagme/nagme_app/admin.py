from django.contrib import admin
from nagme_app.models import Category, UserProfile, Nag


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_author')


class NagAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'author', 'likes', 'created')


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Nag, NagAdmin)
