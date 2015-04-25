from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url('$', 'core.views.app', name='app'),
)
