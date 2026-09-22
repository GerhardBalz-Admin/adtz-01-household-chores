from django import forms

from .models import Chore


class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ["name", "frequency_days"]


class AddAssigneeForm(forms.Form):
    user = forms.ModelChoiceField(queryset=None, label="Household member")

    def __init__(self, *args, household=None, exclude_user_ids=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = household.members.exclude(id__in=exclude_user_ids)
