from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(
        source="assigned_to.username", read_only=True
    )
    assigned_to_name = serializers.CharField(
        source="assigned_to.get_full_name", read_only=True
    )
    is_overdue = serializers.BooleanField(read_only=True)
    time_remaining = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "assigned_to",
            "assigned_to_username",
            "assigned_to_name",
            "status",
            "status_display",
            "deadline",
            "created_at",
            "is_overdue",
            "time_remaining",
        ]
        read_only_fields = ["id", "created_at"]

    def get_time_remaining(self, obj):
        """Calculate time remaining until deadline"""
        if obj.status == "completed":
            return None

        remaining = obj.deadline - timezone.now()
        if remaining.total_seconds() <= 0:
            return None

        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if days > 0:
            return f"{days} days, {hours} hours"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes"
        else:
            return f"{minutes} minutes"

    def validate_assigned_to(self, value):
        """Ensure assigned user has 'member' role"""
        if value.role != "member":
            raise serializers.ValidationError(
                "Tasks can only be assigned to users with 'member' role."
            )
        return value

    def validate_deadline(self, value):
        """Ensure deadline is in the future"""
        if value <= timezone.now():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks (admin only)"""

    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "deadline"]

    def validate_assigned_to(self, value):
        """Ensure assigned user has 'member' role"""
        if value.role != "member":
            raise serializers.ValidationError(
                "Tasks can only be assigned to users with 'member' role."
            )
        return value

    def validate_deadline(self, value):
        """Ensure deadline is in the future"""
        if value <= timezone.now():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tasks (admin only)"""

    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "deadline"]

    def validate_assigned_to(self, value):
        """Ensure assigned user has 'member' role"""
        if value.role != "member":
            raise serializers.ValidationError(
                "Tasks can only be assigned to users with 'member' role."
            )
        return value

    def validate_deadline(self, value):
        """Ensure deadline is in the future for non-completed tasks"""
        if (
            self.instance
            and self.instance.status != "completed"
            and value <= timezone.now()
        ):
            raise serializers.ValidationError(
                "Deadline must be in the future for non-completed tasks."
            )
        return value


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating task status (user only)"""

    class Meta:
        model = Task
        fields = ["status"]

    def validate_status(self, value):
        """Validate status transitions"""
        if not self.instance:
            raise serializers.ValidationError("Task instance is required.")

        current_status = self.instance.status

        # Define valid status transitions
        valid_transitions = {
            "pending": ["in_progress"],
            "in_progress": ["completed"],
            "overdue": ["completed"],
            "completed": [],  # Cannot change from completed
        }

        if value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot change status from '{current_status}' to '{value}'"
            )

        return value


class UserTaskSerializer(serializers.ModelSerializer):
    """Minimal serializer for user dropdown in task assignment"""

    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "full_name"]
