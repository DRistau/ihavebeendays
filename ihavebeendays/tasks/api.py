from django.conf.urls import url
from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from ihavebeendays.tasks.models import Task


class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class TaskResource(ModelResource):
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<uuid>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name='api_dispatch_detail'),
        ]

    class Meta:
        authentication = SessionAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        queryset = Task.objects.all()
        resource_name = 'tasks'
        allowed_methods = ['get']
        excludes = ['id']
        detail_uri_name = 'uuid'
