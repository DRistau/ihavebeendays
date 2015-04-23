from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url('^$', 'core.views.home', name='home'),
    url('app/$', 'core.views.app', name='app'),
    url('login/$', 'core.views.login', name='login'),
    url('logout/$', 'core.views.logout', name='logout'),
)
