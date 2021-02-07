"""abakpress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path

from nestedpages.views import (
    StaticPageView, CreateStaticPageView, EditStaticPageView
)

urlpatterns = [
    re_path(r'^(?P<url>.*)add$', CreateStaticPageView.as_view(), name='create_page'),
    re_path(r'^(?P<url>.*/)edit$', EditStaticPageView.as_view(), name='edit_page'),
    re_path(r'^(?P<url>.*)$', StaticPageView.as_view(), name='page'),
]
