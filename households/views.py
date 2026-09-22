from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CreateHouseholdForm, JoinHouseholdForm
from .models import Household, Membership


@login_required
def choose(request):
    if request.user.households.exists():
        return redirect("households:detail", pk=request.user.households.first().pk)
    create_form = CreateHouseholdForm()
    join_form = JoinHouseholdForm()
    return render(
        request,
        "households/choose.html",
        {"create_form": create_form, "join_form": join_form},
    )


@login_required
def create(request):
    if request.method == "POST":
        form = CreateHouseholdForm(request.POST)
        if form.is_valid():
            household = form.save()
            Membership.objects.create(user=request.user, household=household)
            return redirect("households:detail", pk=household.pk)
    else:
        form = CreateHouseholdForm()
    return render(request, "households/choose.html", {"create_form": form, "join_form": JoinHouseholdForm()})


@login_required
def join(request):
    if request.method == "POST":
        form = JoinHouseholdForm(request.POST)
        if form.is_valid():
            household = Household.objects.get(invite_code=form.cleaned_data["invite_code"])
            Membership.objects.get_or_create(user=request.user, household=household)
            return redirect("households:detail", pk=household.pk)
    else:
        form = JoinHouseholdForm()
    return render(request, "households/choose.html", {"create_form": CreateHouseholdForm(), "join_form": form})


@login_required
def detail(request, pk):
    household = Household.objects.get(pk=pk, members=request.user)
    return render(request, "households/detail.html", {"household": household})
