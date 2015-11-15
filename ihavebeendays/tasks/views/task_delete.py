from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView
from django.contrib import messages
from ihavebeendays.tasks.models import Task


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
