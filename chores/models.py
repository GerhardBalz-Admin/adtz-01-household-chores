from django.conf import settings
from django.db import models
from django.utils import timezone

from households.models import Household


class Chore(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="chores")
    name = models.CharField(max_length=100)
    frequency_days = models.PositiveIntegerField(
        default=7, help_text="How often this chore repeats, in days"
    )
    current_turn_index = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.household})"

    def assignees_ordered(self):
        return self.assignees.select_related("user").order_by("order")

    def current_assignee(self):
        assignees = list(self.assignees_ordered())
        if not assignees:
            return None
        index = self.current_turn_index % len(assignees)
        return assignees[index].user

    def advance_rotation(self):
        count = self.assignees.count()
        if count:
            self.current_turn_index = (self.current_turn_index + 1) % count
            self.save(update_fields=["current_turn_index"])

    def last_completed_at(self):
        completion = self.completions.order_by("-completed_at").first()
        return completion.completed_at if completion else None

    def next_due_at(self):
        base = self.last_completed_at() or self.created_at
        return base + timezone.timedelta(days=self.frequency_days)

    def is_overdue(self):
        return self.next_due_at() < timezone.now()


class ChoreAssignee(models.Model):
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, related_name="assignees")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = ["chore", "user"]

    def __str__(self):
        return f"{self.user} (#{self.order}) for {self.chore}"


class ChoreCompletion(models.Model):
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, related_name="completions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.chore} done by {self.user} at {self.completed_at}"
