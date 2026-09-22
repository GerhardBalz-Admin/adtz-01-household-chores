from django.db import IntegrityError
from django.test import TestCase

from .models import User


class UserManagerTests(TestCase):
    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="pass12345")

    def test_create_user_sets_password_and_defaults(self):
        user = User.objects.create_user(email="a@test.com", password="pass12345")
        self.assertTrue(user.check_password("pass12345"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_sets_flags(self):
        user = User.objects.create_superuser(email="admin@test.com", password="pass12345")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_rejects_is_staff_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@test.com", password="pass12345", is_staff=False
            )

    def test_email_is_unique(self):
        User.objects.create_user(email="dup@test.com", password="pass12345")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="dup@test.com", password="pass12345")
