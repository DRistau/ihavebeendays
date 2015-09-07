from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from tasks.views import (TaskCreateView, TaskDeleteView, TaskDoneView,
                         TaskListView, TaskResetView)


urlpatterns = patterns('',
    url(r'^$', login_required(TaskListView.as_view()), name='tasks'),
    url(r'^add/$', login_required(TaskCreateView.as_view()), name='task-create'),
    url(r'^(?P<uuid>[\w\d_.-]+)/reset/$', login_required(TaskResetView.as_view()), name='task-reset'),
    url(r'^(?P<uuid>[\w\d_.-]+)/done/$', login_required(TaskDoneView.as_view()), name='task-done'),
    url(r'^(?P<uuid>[\w\d_.-]+)/delete/$', login_required(TaskDeleteView.as_view()), name='task-delete'),
)
