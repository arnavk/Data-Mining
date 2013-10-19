from django.conf.urls import patterns, url

from mapper import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^init/$', views.initialize, name='init'),
    #url(r'^search/$', views.search, name="search"),
    url(r'^search/(?P<hashtag>\w+)/$', views.tagsearch),
)