"""nagme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from _nagme import views
from _nagme.views import ReminderCreateView
from _nagme.views import ReminderListView
from _nagme.views import ReminderDeleteView
from _nagme.views import ReminderDetailView

urlpatterns = [
    url(r'^$',
        views.base, name='base'),
    url(r'^welcome/',
        views.welcome, name='welcome'),
    url(r'^login/',
        views.login, name='login'),
    url(r'^registration/',
        views.login, name='registration'),
    url(r'^userhome/',
        views.userhome, name='userhome'),
    url(r'^userhome/account/',
        views.account, name='account'),
    url(r'^userhome/account/account_details/',
        views.account_details, name='account_details'),
    url(r'^userhome/account/account_details/account_password',
        views.account_password, name='account_password'),
    url(r'^userhome/addnag/',
        views.addnag, name='addnag'),
    url(r'^userhome/support/',
        views.support, name='support'),
    url(r'^userhome/categories_list/',
        views.categories, name='categories'),
    url(r'^userhome/category/',
        views.category, name='category'),
    url(r'^add_reminder/$', ReminderCreateView.as_view(), name='new_reminder'),
    url(r'^reminders/$', ReminderListView.as_view(), name='list_reminders'),
    url(r'^(?P<reminder_name_slug>[\w\-]+)/delete$', ReminderDeleteView.as_view(), name='delete_reminder'),
    url(r'^(?P<category_name_slug>[\w\-]+)/$', ReminderDetailView.as_view(), name='detail_reminder'),
]
