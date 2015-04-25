from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url('$', 'tasks.views.app', name='app'),
)
