from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from mapper import views
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('mapper.urls')),
    # url(r'^$', 'Visualiser.views.home', name='home'),
    # url(r'^Visualiser/', include('Visualiser.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)