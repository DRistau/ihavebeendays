from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from ihavebeendays.tasks.api import TaskResource

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^tasks/', include('tasks.urls')),
    url(r'', include('core.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
