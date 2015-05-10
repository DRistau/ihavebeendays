from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
)
