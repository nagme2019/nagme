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
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from nagme_app import views
# from nagme_app.views import ReminderCreateView
# from nagme_app.views import ReminderListView
# from nagme_app.views import ReminderDeleteView
# from nagme_app.views import ReminderDetailView

urlpatterns = [
    url(r'^$',
        views.welcome, name='welcome'),
    url(r'^base/', views.base, name='base'),
    url(r'^log_in/',
        views.log_in, name='log_in'),
    url(r'^registration/',
        views.registration, name='registration'),
    url(r'^user_home/',
        views.user_home, name='user_home'),
    url(r'^user_home/account/',
        views.account, name='account'),
    url(r'^user_home/account/account_details/',
        views.account_details, name='account_details'),
    url(r'^user_home/account/account_details/account_password',
        views.account_password, name='account_password'),
    url(r'^support/',
        views.support, name='support'),
    url(r'^categories_list/',
        views.categories, name='categories'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_nag/$',
        views.add_nag,
        name='add_nag'),
    url(r'^subscribed_categories/$',
        views.subscribed_categories,
        name='subscribed_categories'),
    url(r'^nags/$', views.nags, name='nags'),
    url(r'^admin/', admin.site.urls),
    # url(r'^add_reminder/$', ReminderCreateView.as_view(), name='new_reminder'),
    # url(r'^reminders/$', ReminderListView.as_view(), name='list_reminders'),
    # url(r'^(?P<reminder_name_slug>[\w\-]+)/delete$', ReminderDeleteView.as_view(), name='delete_reminder'),
    # url(r'^(?P<category_name_slug>[\w\-]+)/$', ReminderDetailView.as_view(), name='detail_reminder'),
]
