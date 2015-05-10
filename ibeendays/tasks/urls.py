from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from tasks.views import (TaskCreateView, TaskDoneView, TaskListView,
                         TaskResetView)


urlpatterns = patterns('',
    url(r'^$', login_required(TaskListView.as_view()), name='tasks'),
    url(r'^add/$', login_required(TaskCreateView.as_view()), name='task-create'),
    url(r'^(?P<pk>\d+)/reset/$', login_required(TaskResetView.as_view()), name='task-reset'),
    url(r'^(?P<pk>\d+)/done/$', login_required(TaskDoneView.as_view()), name='task-done'),
)
