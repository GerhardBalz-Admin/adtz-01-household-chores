from django.test import TestCase

from accounts.models import User

from .models import Household, Membership


class HouseholdModelTests(TestCase):
    def test_invite_code_is_generated_and_unique(self):
        h1 = Household.objects.create(name="House 1")
        h2 = Household.objects.create(name="House 2")
        self.assertTrue(h1.invite_code)
        self.assertNotEqual(h1.invite_code, h2.invite_code)


class HouseholdViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="a@test.com", password="pass12345")
        self.other = User.objects.create_user(email="b@test.com", password="pass12345")
        self.client.force_login(self.user)

    def test_create_household_creates_membership(self):
        response = self.client.post("/households/create/", {"name": "New House"})
        household = Household.objects.get(name="New House")
        self.assertRedirects(response, f"/households/{household.pk}/")
        self.assertTrue(
            Membership.objects.filter(user=self.user, household=household).exists()
        )

    def test_join_with_valid_invite_code(self):
        household = Household.objects.create(name="Existing House")
        response = self.client.post(
            "/households/join/", {"invite_code": household.invite_code}
        )
        self.assertRedirects(response, f"/households/{household.pk}/")
        self.assertTrue(
            Membership.objects.filter(user=self.user, household=household).exists()
        )

    def test_join_with_invalid_invite_code_rejected(self):
        response = self.client.post("/households/join/", {"invite_code": "bogus"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Membership.objects.filter(user=self.user).exists())

    def test_joining_twice_does_not_duplicate_membership(self):
        household = Household.objects.create(name="Existing House")
        self.client.post("/households/join/", {"invite_code": household.invite_code})
        self.client.post("/households/join/", {"invite_code": household.invite_code})
        self.assertEqual(
            Membership.objects.filter(user=self.user, household=household).count(), 1
        )

    def test_choose_redirects_to_existing_household(self):
        household = Household.objects.create(name="Existing House")
        Membership.objects.create(user=self.user, household=household)
        response = self.client.get("/households/")
        self.assertRedirects(response, f"/households/{household.pk}/")

    def test_detail_hidden_from_non_member(self):
        household = Household.objects.create(name="Private House")
        Membership.objects.create(user=self.other, household=household)
        response = self.client.get(f"/households/{household.pk}/")
        self.assertEqual(response.status_code, 404)
