from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Task



class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)