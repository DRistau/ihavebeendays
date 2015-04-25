from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url('^$', 'core.views.home', name='home'),
    url('^app/$', 'core.views.app', name='app'),
    url('^login/$', 'django.contrib.auth.views.login', name='login'),
    url('^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
)
