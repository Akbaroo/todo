from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs["task_id"], user=self.request.user)
