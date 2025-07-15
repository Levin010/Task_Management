from django.urls import path
from . import views

urlpatterns = [
    path("tasks/", views.TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/status/", views.update_task_status, name="update-task-status"),
    path("tasks/<int:pk>/start/", views.start_task, name="start-task"),
    path("tasks/<int:pk>/complete/", views.complete_task, name="complete-task"),
    path("my-tasks/", views.get_my_tasks, name="my-tasks"),
    path("available-users/", views.get_available_users, name="available-users"),
    path("all-tasks/", views.get_all_tasks, name="all-tasks"),
    path("task-statistics/", views.get_task_statistics, name="task-statistics"),
    path(
        "update-overdue-tasks/", views.update_overdue_tasks, name="update-overdue-tasks"
    ),
]
