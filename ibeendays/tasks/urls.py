from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from tasks.views import TaskCreateView, TaskListView


urlpatterns = patterns('',
    url('$', login_required(TaskListView.as_view()), name='tasks'),
    url('add/$', login_required(TaskCreateView.as_view()), name='task-create'),
)
