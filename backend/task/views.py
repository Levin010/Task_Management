from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from .models import Task
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskStatusUpdateSerializer,
    UserTaskSerializer,
)

User = get_user_model()


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_admin


class TaskListCreateView(generics.ListCreateAPIView):
    """
    List all tasks (admin sees all, users see only their assigned tasks)
    Create new tasks (admin only)
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        else:
            return Task.objects.filter(assigned_to=user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        # Only admins can create tasks
        if not self.request.user.is_admin:
            raise PermissionError("Only admin users can create tasks.")
        serializer.save()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a task
    Admin can perform all operations
    Users can only view tasks assigned to them
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        else:
            return Task.objects.filter(assigned_to=user)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return TaskUpdateSerializer
        return TaskSerializer

    def perform_update(self, serializer):
        if not self.request.user.is_admin:
            raise PermissionError("Only admin users can update task details.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_admin:
            raise PermissionError("Only admin users can delete tasks.")
        instance.delete()


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_task_status(request, pk):
    """
    Update task status (users can only update their own assigned tasks)
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_admin and task.assigned_to != request.user:
        return Response(
            {"detail": "You can only update tasks assigned to you."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = TaskStatusUpdateSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        task_serializer = TaskSerializer(task)
        return Response(task_serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_task(request, pk):
    """
    Start a task (change status from pending to in_progress)
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_admin and task.assigned_to != request.user:
        return Response(
            {"detail": "You can only start tasks assigned to you."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if task.status != "pending":
        return Response(
            {"detail": f"Cannot start task with status '{task.status}'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    task.status = "in_progress"
    task.save()

    task_serializer = TaskSerializer(task)
    return Response(task_serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_task(request, pk):
    """
    Complete a task (change status to completed)
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_admin and task.assigned_to != request.user:
        return Response(
            {"detail": "You can only complete tasks assigned to you."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if task.status in ["completed"]:
        return Response(
            {"detail": "Task is already completed."}, status=status.HTTP_400_BAD_REQUEST
        )

    task.status = "completed"
    task.save()

    task_serializer = TaskSerializer(task)
    return Response(task_serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAdmin])
def get_available_users(request):
    """
    Get list of users with 'user' role for task assignment (admin only)
    """
    users = User.objects.filter(role="user")
    serializer = UserTaskSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_tasks(request):
    """
    Get tasks assigned to the current user
    """
    if request.user.is_admin:
        return Response(
            {"detail": "This endpoint is for regular users only."},
            status=status.HTTP_403_FORBIDDEN,
        )

    tasks = Task.objects.filter(assigned_to=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAdmin])
def get_all_tasks(request):
    """
    Get all tasks (admin only)
    """
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task_statistics(request):
    """
    Get task statistics
    """
    user = request.user

    if user.is_admin:
        total_tasks = Task.objects.count()
        pending_tasks = Task.objects.filter(status="pending").count()
        in_progress_tasks = Task.objects.filter(status="in_progress").count()
        completed_tasks = Task.objects.filter(status="completed").count()
        overdue_tasks = Task.objects.filter(status="overdue").count()
    else:
        user_tasks = Task.objects.filter(assigned_to=user)
        total_tasks = user_tasks.count()
        pending_tasks = user_tasks.filter(status="pending").count()
        in_progress_tasks = user_tasks.filter(status="in_progress").count()
        completed_tasks = user_tasks.filter(status="completed").count()
        overdue_tasks = user_tasks.filter(status="overdue").count()

    return Response(
        {
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_overdue_tasks(request):
    """
    Update tasks that are past their deadline to overdue status
    This can be called periodically or manually
    """
    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now(), status__in=["pending", "in_progress"]
    )

    updated_count = overdue_tasks.update(status="overdue")

    return Response(
        {
            "message": f"Updated {updated_count} tasks to overdue status",
            "updated_count": updated_count,
        },
        status=status.HTTP_200_OK,
    )
