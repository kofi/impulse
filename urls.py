from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django import template
template.add_to_builtins('israel.templatetags.israel_forms')


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'impulse.views.home', name='home'),
    # url(r'^impulse/', include('impulse.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT }),
    (r'^g/', include('impulse.gelder.urls')),
    (r'^j/', include('impulse.juno.urls')),
)
