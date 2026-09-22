from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from households.models import Household

from .forms import AddAssigneeForm, ChoreForm
from .models import Chore, ChoreAssignee, ChoreCompletion


def _get_household(request, household_pk):
    return get_object_or_404(Household, pk=household_pk, members=request.user)


def _get_chore(request, household_pk, pk):
    household = _get_household(request, household_pk)
    return household, get_object_or_404(Chore, pk=pk, household=household)


@login_required
def chore_list(request, household_pk):
    household = _get_household(request, household_pk)
    chores = household.chores.all()
    return render(
        request, "chores/chore_list.html", {"household": household, "chores": chores}
    )


@login_required
def chore_create(request, household_pk):
    household = _get_household(request, household_pk)
    if request.method == "POST":
        form = ChoreForm(request.POST)
        if form.is_valid():
            chore = form.save(commit=False)
            chore.household = household
            chore.save()
            return redirect("chores:detail", household_pk=household.pk, pk=chore.pk)
    else:
        form = ChoreForm()
    return render(
        request, "chores/chore_form.html", {"household": household, "form": form}
    )


@login_required
def chore_update(request, household_pk, pk):
    household, chore = _get_chore(request, household_pk, pk)
    if request.method == "POST":
        form = ChoreForm(request.POST, instance=chore)
        if form.is_valid():
            form.save()
            return redirect("chores:detail", household_pk=household.pk, pk=chore.pk)
    else:
        form = ChoreForm(instance=chore)
    return render(
        request,
        "chores/chore_form.html",
        {"household": household, "form": form, "chore": chore},
    )


@login_required
def chore_delete(request, household_pk, pk):
    household, chore = _get_chore(request, household_pk, pk)
    if request.method == "POST":
        chore.delete()
        return redirect("chores:list", household_pk=household.pk)
    return render(
        request, "chores/chore_confirm_delete.html", {"household": household, "chore": chore}
    )


@login_required
def chore_detail(request, household_pk, pk):
    household, chore = _get_chore(request, household_pk, pk)
    assignees = list(chore.assignees_ordered())
    add_form = AddAssigneeForm(
        household=household, exclude_user_ids=[a.user_id for a in assignees]
    )
    return render(
        request,
        "chores/chore_detail.html",
        {
            "household": household,
            "chore": chore,
            "assignees": assignees,
            "current_assignee": chore.current_assignee(),
            "add_form": add_form,
            "completions": chore.completions.select_related("user")[:5],
        },
    )


@login_required
def chore_mark_done(request, household_pk, pk):
    household, chore = _get_chore(request, household_pk, pk)
    if request.method == "POST":
        ChoreCompletion.objects.create(chore=chore, user=request.user)
        chore.advance_rotation()
    return redirect("chores:detail", household_pk=household.pk, pk=chore.pk)


@login_required
def assignee_add(request, household_pk, pk):
    household, chore = _get_chore(request, household_pk, pk)
    existing_ids = [a.user_id for a in chore.assignees_ordered()]
    if request.method == "POST":
        form = AddAssigneeForm(request.POST, household=household, exclude_user_ids=existing_ids)
        if form.is_valid():
            next_order = chore.assignees.count()
            ChoreAssignee.objects.create(
                chore=chore, user=form.cleaned_data["user"], order=next_order
            )
    return redirect("chores:detail", household_pk=household.pk, pk=chore.pk)


@login_required
def assignee_remove(request, household_pk, pk, assignee_pk):
    household, chore = _get_chore(request, household_pk, pk)
    if request.method == "POST":
        get_object_or_404(ChoreAssignee, pk=assignee_pk, chore=chore).delete()
        for index, assignee in enumerate(chore.assignees_ordered()):
            if assignee.order != index:
                assignee.order = index
                assignee.save(update_fields=["order"])
        if chore.current_turn_index >= max(chore.assignees.count(), 1):
            chore.current_turn_index = 0
            chore.save(update_fields=["current_turn_index"])
    return redirect("chores:detail", household_pk=household.pk, pk=chore.pk)


@login_required
def assignee_move(request, household_pk, pk, assignee_pk, direction):
    household, chore = _get_chore(request, household_pk, pk)
    if request.method == "POST":
        assignees = list(chore.assignees_ordered())
        index = next(i for i, a in enumerate(assignees) if a.pk == int(assignee_pk))
        swap_with = index - 1 if direction == "up" else index + 1
        if 0 <= swap_with < len(assignees):
            a, b = assignees[index], assignees[swap_with]
            a.order, b.order = b.order, a.order
            a.save(update_fields=["order"])
            b.save(update_fields=["order"])
    return redirect("chores:detail", household_pk=household.pk, pk=chore.pk)


@login_required
def household_history(request, household_pk):
    household = _get_household(request, household_pk)
    completions = ChoreCompletion.objects.filter(chore__household=household).select_related(
        "chore", "user"
    )
    return render(
        request,
        "chores/household_history.html",
        {"household": household, "completions": completions},
    )
