from django.core.management.base import BaseCommand
from django.utils import timezone
from task.models import Task


class Command(BaseCommand):
    help = "Update tasks that are past their deadline to overdue status"

    def handle(self, *args, **options):
        # Find tasks that are past deadline and not completed
        overdue_tasks = Task.objects.filter(
            deadline__lt=timezone.now(), status__in=["pending", "in_progress"]
        )

        updated_count = overdue_tasks.update(status="overdue")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {updated_count} tasks to overdue status"
            )
        )

        if updated_count > 0:
            self.stdout.write("Updated tasks:")
            for task in overdue_tasks:
                self.stdout.write(
                    f"  - {task.title} (assigned to {task.assigned_to.username})"
                )
        else:
            self.stdout.write("No tasks needed to be updated.")
