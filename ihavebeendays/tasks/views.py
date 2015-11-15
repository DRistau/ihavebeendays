from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages
from ihavebeendays.tasks.forms import TaskForm, TaskResetForm
from ihavebeendays.tasks.models import Task


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
    http_method_names = ['post']
    form_class = TaskForm
    model = Task

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)

        messages.success(self.request, 'Task created!')

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('tasks')

    def post(self, *args, **kwargs):
        return super(TaskCreateView, self).post(*args, **kwargs)


class TaskResetView(UpdateView):
    model = Task
    form_class = TaskResetForm
    template_name = 'tasks/task_reset_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            form.reset()
            messages.success(self.request, 'Task reseted!')

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 uuid=self.kwargs.get('uuid'))

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

        messages.success(self.request, 'Task done!')

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 uuid=self.kwargs.get('uuid'))

    def get_queryset(self):
        qs = super(TaskDoneView, self).get_queryset()
        return qs.filter(user=self.request.user).unfinished()

    def get_success_url(self):
        return reverse('tasks')


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

    def get(self, request, *args, **kwargs):
        messages.success(self.request, 'Task removed!')

        return self.delete(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 uuid=self.kwargs.get('uuid'))

    def get_queryset(self):
        qs = super(TaskDeleteView, self).get_queryset()
        return qs.filter(user=self.request.user).finished()
