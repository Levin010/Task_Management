from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("overdue", "Overdue"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
        limit_choices_to={"role": "member"},
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks",
        limit_choices_to={"role__in": ["admin", "manager"]},
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"

    def save(self, *args, **kwargs):
        if self.deadline < timezone.now() and self.status not in [
            "completed",
            "overdue",
        ]:
            self.status = "overdue"

        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        return self.deadline < timezone.now() and self.status not in ["completed"]

    @property
    def time_remaining(self):
        """Get time remaining until deadline"""
        if self.status == "completed":
            return None

        remaining = self.deadline - timezone.now()
        return remaining if remaining.total_seconds() > 0 else None
