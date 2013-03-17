from django.conf.urls import patterns, include, url

from myapp.views import TestView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TestView.as_view()),
)


from tastypie.api import Api

from myapp.api import BookResource


v1_api = Api(api_name='v1')
v1_api.register(BookResource())

urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),
)
