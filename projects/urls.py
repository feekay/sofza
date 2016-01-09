from django.conf.urls import  patterns, url
from projects import views

urlpatterns = patterns('',
    url(r'^$', views.projects, name = 'projects'),
    url(r'^logout/$', views.logout_view, name = 'projects'),
    url(r'^(?P<year>[2][0][0-9][0-9])/(?P<month>[a-z][a-z][a-z])/$', views.projects, name= 'projects'),# Valid till 2099
    url(r'^analytics/$', views.analytics, name='analytics'),
    url(r'^staff/$', views.staff, name='staff'),
    url(r'^(?P<project_id>[\w\-]+)/invoice/$', views.invoice, name= 'invoice'),
    url(r'^(?P<project_id>[\w\-]+)/(?P<mile_id>[\w\-]+)/$', views.milestone_page, name= 'milestone_page'),
    url(r'^(?P<project_id>[\w\-]+)/$', views.project_page, name= 'project_page'),
)


