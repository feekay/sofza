"""sofza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from projects import views
from mysite import views as site_views
urlpatterns = [
    url(r'^11111111/', include(admin.site.urls)),
    url(r'^site/', include('mysite.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^$', site_views.index, name="home"),
    url(r'^faq$', site_views.faq, name="faq"),
    url(r'^portfolio$', site_views.portfolio, name="portfolio"),
    url(r'^about$', site_views.about, name="about"),
    url(r'^policy$', site_views.policy, name="policy"),
    url(r'^contact$', site_views.contact, name="contact"),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', views.download_file, {
        'document_root': settings.MEDIA_ROOT}))
