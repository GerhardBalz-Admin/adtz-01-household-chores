from django.urls import path

from . import views

app_name = "chores"

urlpatterns = [
    path("<int:household_pk>/chores/", views.chore_list, name="list"),
    path("<int:household_pk>/chores/new/", views.chore_create, name="create"),
    path("<int:household_pk>/chores/<int:pk>/", views.chore_detail, name="detail"),
    path("<int:household_pk>/chores/<int:pk>/edit/", views.chore_update, name="update"),
    path("<int:household_pk>/chores/<int:pk>/delete/", views.chore_delete, name="delete"),
    path("<int:household_pk>/chores/<int:pk>/done/", views.chore_mark_done, name="mark-done"),
    path("<int:household_pk>/history/", views.household_history, name="history"),
    path(
        "<int:household_pk>/chores/<int:pk>/assignees/add/",
        views.assignee_add,
        name="assignee-add",
    ),
    path(
        "<int:household_pk>/chores/<int:pk>/assignees/<int:assignee_pk>/remove/",
        views.assignee_remove,
        name="assignee-remove",
    ),
    path(
        "<int:household_pk>/chores/<int:pk>/assignees/<int:assignee_pk>/move/<str:direction>/",
        views.assignee_move,
        name="assignee-move",
    ),
]
