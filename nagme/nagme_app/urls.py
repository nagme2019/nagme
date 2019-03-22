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

urlpatterns = [
    url(r'^$',
        views.welcome, name='welcome'),
    url(r'^base/', views.base, name='base'),
    # url(r'^log_in/',
    #     views.log_in, name='log_in'),
    # url(r'^registration/',
    #     views.registration, name='registration'),
    # url(r'^log_out/$',
    #     views.log_out, name="log_out"),
    url(r'^user_home/',
        views.user_home, name='user_home'),
    url(r'^account/',
        views.account, name='account'),
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
    url(r'^nags/by_time$', views.nags_time, name='nags_time'),
    url(r'^nags/by_likes$', views.nags_likes, name='nags_likes'),
    url(r'^admin/', admin.site.urls),
    url(r'^subscribe/', views.subscribe, name='subscribe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
