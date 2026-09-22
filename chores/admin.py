from django.contrib import admin

from .models import Chore, ChoreAssignee, ChoreCompletion


class ChoreAssigneeInline(admin.TabularInline):
    model = ChoreAssignee
    extra = 0


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ["name", "household", "frequency_days", "current_turn_index"]
    list_filter = ["household"]
    inlines = [ChoreAssigneeInline]


@admin.register(ChoreCompletion)
class ChoreCompletionAdmin(admin.ModelAdmin):
    list_display = ["chore", "user", "completed_at"]
    list_filter = ["chore__household"]
