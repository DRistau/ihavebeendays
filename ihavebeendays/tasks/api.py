from django.conf.urls import url
from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from ihavebeendays.tasks.models import Task


class TaskResource(ModelResource):
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<uuid>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name='api_dispatch_detail'),
        ]

    class Meta:
        queryset = Task.objects.all()
        resource_name = 'tasks'
        allowed_methods = ['get']
        excludes = ['id']
        detail_uri_name = 'uuid'
        authentication = SessionAuthentication()
