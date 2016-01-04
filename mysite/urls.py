from django.conf.urls import  patterns, url
from mysite import views

urlpatterns = patterns('',
        url(r'^$', views.index, name = 'index'),
        url(r'^portfolio/$', views.portfolio, name= 'portfolio'),
        url(r'^faq/$', views.faq, name ='faq'),
)
