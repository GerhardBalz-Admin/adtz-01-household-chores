from django.contrib import admin

from .models import Chore, ChoreAssignee


class ChoreAssigneeInline(admin.TabularInline):
    model = ChoreAssignee
    extra = 0


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ["name", "household", "frequency_days", "current_turn_index"]
    list_filter = ["household"]
    inlines = [ChoreAssigneeInline]
