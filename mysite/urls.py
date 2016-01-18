from django.conf.urls import  patterns, url
from mysite import views

urlpatterns = patterns('',
        url(r'^$', views.index, name = 'index'),
        url(r'^portfolio/$', views.portfolio, name= 'portfolio'),
        url(r'^faq/$', views.faq, name ='faq'),
        url(r'^email_data/$', views.emails, name ='emails'),
        url(r'^about/$', views.about, name ='about'),
        url(r'^policy/$', views.policy, name ='policy'),
)
