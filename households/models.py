import secrets

from django.conf import settings
from django.db import models


def generate_invite_code():
    return secrets.token_urlsafe(8)


class Household(models.Model):
    name = models.CharField(max_length=100)
    invite_code = models.CharField(
        max_length=32, unique=True, default=generate_invite_code, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Membership", related_name="households"
    )

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "household"]

    def __str__(self):
        return f"{self.user} in {self.household}"
