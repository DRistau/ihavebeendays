from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework import permissions, viewsets
from ihavebeendays.tasks.forms import TaskForm
from ihavebeendays.tasks.models import Task
from ihavebeendays.tasks.permissions import IsOwnerPermission
from ihavebeendays.tasks.serializers import TaskSerializer


class TaskListView(ListView):
    model = Task

    def get_queryset(self, *args, **kwargs):
        qs = super(TaskListView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user).finished()

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['task_started'] = self.model.objects.filter(user=self.request.user).unfinished()
        context['task_form'] = TaskForm()

        return context


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    http_method_names = ['post']

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('tasks')

    def post(self, *args, **kwargs):
        return super(TaskCreateView, self).post(*args, **kwargs)


class TaskResetView(UpdateView):
    model = Task
    form_class = TaskForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.reset()

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 pk=self.kwargs.get('pk'))

    def get_queryset(self):
        qs = super(TaskResetView, self).get_queryset()
        return qs.filter(user=self.request.user).unfinished()

    def get_success_url(self):
        return reverse('tasks')


class TaskDoneView(UpdateView):
    model = Task
    form_class = TaskForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.done()

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 pk=self.kwargs.get('pk'))

    def get_queryset(self):
        qs = super(TaskDoneView, self).get_queryset()
        return qs.filter(user=self.request.user).unfinished()

    def get_success_url(self):
        return reverse('tasks')


class TaskViewSet(viewsets.ModelViewSet):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerPermission)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
