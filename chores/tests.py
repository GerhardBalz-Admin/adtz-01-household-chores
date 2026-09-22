from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from households.models import Household, Membership

from .models import Chore, ChoreAssignee, ChoreCompletion


class ChoreRotationTests(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="Rotation House")
        self.u1 = User.objects.create_user(email="a@test.com", password="pass12345")
        self.u2 = User.objects.create_user(email="b@test.com", password="pass12345")
        self.chore = Chore.objects.create(household=self.household, name="Dishes")

    def test_current_assignee_none_when_empty(self):
        self.assertIsNone(self.chore.current_assignee())

    def test_current_assignee_follows_order(self):
        ChoreAssignee.objects.create(chore=self.chore, user=self.u2, order=0)
        ChoreAssignee.objects.create(chore=self.chore, user=self.u1, order=1)
        self.assertEqual(self.chore.current_assignee(), self.u2)

    def test_current_assignee_wraps_with_modulo(self):
        ChoreAssignee.objects.create(chore=self.chore, user=self.u1, order=0)
        ChoreAssignee.objects.create(chore=self.chore, user=self.u2, order=1)
        self.chore.current_turn_index = 5
        self.assertEqual(self.chore.current_assignee(), self.u2)

    def test_advance_rotation_cycles(self):
        ChoreAssignee.objects.create(chore=self.chore, user=self.u1, order=0)
        ChoreAssignee.objects.create(chore=self.chore, user=self.u2, order=1)
        self.assertEqual(self.chore.current_assignee(), self.u1)
        self.chore.advance_rotation()
        self.assertEqual(self.chore.current_assignee(), self.u2)
        self.chore.advance_rotation()
        self.assertEqual(self.chore.current_assignee(), self.u1)

    def test_advance_rotation_noop_when_no_assignees(self):
        self.chore.advance_rotation()
        self.assertEqual(self.chore.current_turn_index, 0)


class ChoreDueDateTests(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="Due Date House")
        self.user = User.objects.create_user(email="a@test.com", password="pass12345")

    def test_next_due_at_uses_created_at_when_never_completed(self):
        chore = Chore.objects.create(household=self.household, name="Trash", frequency_days=3)
        self.assertEqual(chore.next_due_at(), chore.created_at + timedelta(days=3))

    def test_next_due_at_uses_last_completion(self):
        chore = Chore.objects.create(household=self.household, name="Trash", frequency_days=3)
        completion = ChoreCompletion.objects.create(chore=chore, user=self.user)
        self.assertEqual(chore.next_due_at(), completion.completed_at + timedelta(days=3))

    def test_is_overdue_false_for_future_due_date(self):
        chore = Chore.objects.create(household=self.household, name="Trash", frequency_days=7)
        self.assertFalse(chore.is_overdue())

    def test_is_overdue_true_for_past_due_date(self):
        chore = Chore.objects.create(household=self.household, name="Trash", frequency_days=1)
        Chore.objects.filter(pk=chore.pk).update(
            created_at=timezone.now() - timedelta(days=5)
        )
        chore.refresh_from_db()
        self.assertTrue(chore.is_overdue())


class ChoreViewTests(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="View House")
        self.user = User.objects.create_user(email="a@test.com", password="pass12345")
        self.outsider = User.objects.create_user(email="out@test.com", password="pass12345")
        Membership.objects.create(user=self.user, household=self.household)
        self.chore = Chore.objects.create(household=self.household, name="Dishes")
        self.client.force_login(self.user)

    def test_anonymous_user_redirected_to_login(self):
        self.client.logout()
        response = self.client.get(f"/households/{self.household.pk}/chores/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_non_member_gets_404(self):
        self.client.force_login(self.outsider)
        response = self.client.get(f"/households/{self.household.pk}/chores/")
        self.assertEqual(response.status_code, 404)

    def test_create_chore(self):
        response = self.client.post(
            f"/households/{self.household.pk}/chores/new/",
            {"name": "Vacuum", "frequency_days": 5},
        )
        chore = Chore.objects.get(household=self.household, name="Vacuum")
        self.assertRedirects(
            response, f"/households/{self.household.pk}/chores/{chore.pk}/"
        )
        self.assertEqual(chore.frequency_days, 5)

    def test_update_chore(self):
        self.client.post(
            f"/households/{self.household.pk}/chores/{self.chore.pk}/edit/",
            {"name": "Dishes", "frequency_days": 2},
        )
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.frequency_days, 2)

    def test_delete_chore(self):
        self.client.post(f"/households/{self.household.pk}/chores/{self.chore.pk}/delete/")
        self.assertFalse(Chore.objects.filter(pk=self.chore.pk).exists())

    def test_mark_done_creates_completion_and_advances_rotation(self):
        ChoreAssignee.objects.create(chore=self.chore, user=self.user, order=0)
        other = User.objects.create_user(email="c@test.com", password="pass12345")
        Membership.objects.create(user=other, household=self.household)
        ChoreAssignee.objects.create(chore=self.chore, user=other, order=1)

        self.client.post(f"/households/{self.household.pk}/chores/{self.chore.pk}/done/")

        self.assertEqual(ChoreCompletion.objects.filter(chore=self.chore).count(), 1)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.current_assignee(), other)

    def test_mark_done_ignores_get(self):
        ChoreAssignee.objects.create(chore=self.chore, user=self.user, order=0)
        self.client.get(f"/households/{self.household.pk}/chores/{self.chore.pk}/done/")
        self.assertEqual(ChoreCompletion.objects.filter(chore=self.chore).count(), 0)

    def test_assignee_add_and_remove_reindexes_order(self):
        other = User.objects.create_user(email="c@test.com", password="pass12345")
        Membership.objects.create(user=other, household=self.household)

        self.client.post(
            f"/households/{self.household.pk}/chores/{self.chore.pk}/assignees/add/",
            {"user": self.user.pk},
        )
        self.client.post(
            f"/households/{self.household.pk}/chores/{self.chore.pk}/assignees/add/",
            {"user": other.pk},
        )
        first = ChoreAssignee.objects.get(chore=self.chore, user=self.user)
        self.client.post(
            f"/households/{self.household.pk}/chores/{self.chore.pk}"
            f"/assignees/{first.pk}/remove/"
        )
        remaining = list(self.chore.assignees_ordered())
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].user, other)
        self.assertEqual(remaining[0].order, 0)

    def test_assignee_move_swaps_order(self):
        a1 = ChoreAssignee.objects.create(chore=self.chore, user=self.user, order=0)
        other = User.objects.create_user(email="c@test.com", password="pass12345")
        Membership.objects.create(user=other, household=self.household)
        a2 = ChoreAssignee.objects.create(chore=self.chore, user=other, order=1)

        self.client.post(
            f"/households/{self.household.pk}/chores/{self.chore.pk}"
            f"/assignees/{a2.pk}/move/up/"
        )
        a1.refresh_from_db()
        a2.refresh_from_db()
        self.assertEqual(a2.order, 0)
        self.assertEqual(a1.order, 1)

    def test_removing_assignee_resets_out_of_range_turn_index(self):
        ChoreAssignee.objects.create(chore=self.chore, user=self.user, order=0)
        other = User.objects.create_user(email="c@test.com", password="pass12345")
        Membership.objects.create(user=other, household=self.household)
        ChoreAssignee.objects.create(chore=self.chore, user=other, order=1)
        self.chore.current_turn_index = 1
        self.chore.save(update_fields=["current_turn_index"])

        self.client.post(
            f"/households/{self.household.pk}/chores/{self.chore.pk}"
            f"/assignees/{ChoreAssignee.objects.get(chore=self.chore, user=other).pk}/remove/"
        )
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.current_turn_index, 0)

    def test_household_history_lists_completions(self):
        ChoreCompletion.objects.create(chore=self.chore, user=self.user)
        response = self.client.get(f"/households/{self.household.pk}/history/")
        self.assertContains(response, "Dishes")
