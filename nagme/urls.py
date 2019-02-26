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
from nagme import views

urlpatterns = [
    url(r'^welcome/',
        views.welcome, name ='welcome'),
    url(r'^login/',
        views.login,  name= 'login'),
    url(r'^registration/',
        views.login, name='registration'),
    url(r'^userhome/',
        views.userhome, name='userhome'),
    url(r'^userhome/account/',
        views.acount, name='account'),
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
        views.category, name='category')
]
