from django.conf.urls import  patterns, url
from projects import views

urlpatterns = patterns('',
    url(r'^$', views.projects, name = 'projects'),
    url(r'^(?P<project_id>[\w\-]+)/(?P<name>[\w\-]+)/$', views.milestone_page, name= 'milestone_page'),
    url(r'^(?P<project_id>[\w\-]+)/$', views.project_page, name= 'project_page'),
)


