from tastypie.resources import ModelResource
from ihavebeendays.tasks.models import Task


class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'tasks'
        allowed_methods = ['get']
