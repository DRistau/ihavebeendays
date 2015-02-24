from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'ibeendays.views.home', name='home'),
    url(r'^login/$', 'ibeendays.views.login', name='login'),

    # url(r'^admin/', include(admin.site.urls)),
)
