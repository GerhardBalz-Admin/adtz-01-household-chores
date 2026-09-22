from django.contrib import admin

from .models import Household, Membership


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ["name", "invite_code", "created_at"]
    inlines = [MembershipInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "household", "joined_at"]
