from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:task_id>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:task_id>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]