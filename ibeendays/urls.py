from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url('', include('core.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
