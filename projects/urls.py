from django.conf.urls import  patterns, url
from projects import views

urlpatterns = patterns('',
    url(r'^$', views.projects, name = 'projects'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
    url(r'^invoices/$', views.invoice_list, name = 'invoice_list'),
    url(r'^get/(?P<project_id>[\w\-]+)/$', views.get_messages, name='get_messages'),
    url(r'^send/(?P<project_id>[\w\-]+)/$', views.send_message, name='send_message'),
    url(r'^list/(?P<project_id>[\w\-]+)/$', views.person_list, name='person_list'),
    url(r'^suggest_staff/$', views.suggest_staff, name = 'suggest_staff'),
    url(r'^persons/(?P<person_id>[\w\-\_]+)/$', views.get_person, name = 'person_detail'),
    url(r'^(?P<year>[2][0][0-9][0-9])/(?P<month>[a-z][a-z][a-z])/$', views.projects, name= 'projects'),# Valid till 2099
    url(r'^analytics/$', views.analytics, name='analytics'),
    url(r'^staff/$', views.staff, name='staff'),
    url(r'^(?P<project_id>[\w\-]+)/invoice/$', views.invoice, name= 'invoice'),
    url(r'^(?P<project_id>[\w\-]+)/(?P<mile_id>[\w\-]+)/$', views.milestone_page, name= 'milestone_page'),
    url(r'^(?P<project_id>[\w\-]+)/$', views.project_page, name= 'project_page'),
)


