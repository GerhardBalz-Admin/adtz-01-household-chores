from django import forms

from .models import Household


class CreateHouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ["name"]


class JoinHouseholdForm(forms.Form):
    invite_code = forms.CharField(max_length=32)

    def clean_invite_code(self):
        code = self.cleaned_data["invite_code"].strip()
        if not Household.objects.filter(invite_code=code).exists():
            raise forms.ValidationError("No household matches that invite code.")
        return code
