from django.conf.urls import url
from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from ihavebeendays.tasks.models import Task


class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        try:
            instance_user = bundle.obj.user
        except:
            return True

        return instance_user == bundle.request.user


class TaskResource(ModelResource):
    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>{0})/schema/$".format(self._meta.resource_name),
                self.wrap_view('get_schema'),
                name='api_get_schema',
            ),
            url(
                r"^(?P<resource_name>{0})/(?P<uuid>[\w\d_.-]+)/$".format(self._meta.resource_name),
                self.wrap_view('dispatch_detail'),
                name='api_dispatch_detail',
            ),
        ]

    class Meta:
        authentication = SessionAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        queryset = Task.objects.all()
        resource_name = 'tasks'
        allowed_methods = ['get']
        excludes = ['id']
        detail_uri_name = 'uuid'
