from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from tasks.views import TaskListView


urlpatterns = patterns('',
    url('$', login_required(TaskListView.as_view()), name='tasks'),
)
