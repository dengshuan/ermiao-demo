from django.conf.urls import patterns, include, url
from ermiao import views

urlpatterns = patterns('',
                       url(r'^login$', views.login_view, name='login'),
                       url(r'^logout$', views.logout_view, name='logout'),
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^comment$', views.add_comment, name='comment'),
                       url(r'^topic$', views.create_topic, name='topic'),
                       url(r'^like$', views.tag_like, name='like'),
                   )
