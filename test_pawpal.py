import json
import unittest
from datetime import date as Date, time as Time
from unittest.mock import MagicMock, patch

from pawpal_system import Pet, Owner, PetCareTask, Scheduler


# ---------------------------------------------------------------------------
# Helper: mirrors the conflict-detection logic in app.py
# ---------------------------------------------------------------------------
def has_conflict(existing_tasks, new_date, new_time):
    """Return the conflicting task if one exists at the same date+time, else None."""
    return next(
        (t for t in existing_tasks if t.date == new_date and t.start_time == new_time),
        None,
    )


# ---------------------------------------------------------------------------
# 1. Adding pets, owners, tasks
# ---------------------------------------------------------------------------
class TestCoreCreation(unittest.TestCase):

    def test_create_pet(self):
        pet = Pet("Buddy", "dog")
        self.assertEqual(pet.get_name(), "Buddy")
        self.assertEqual(pet.get_type(), "dog")

    def test_create_owner(self):
        owner = Owner("Alice")
        self.assertEqual(owner.get_name(), "Alice")
        self.assertEqual(owner.get_pets(), [])
        self.assertEqual(owner.get_pet_count(), 0)

    def test_create_task_defaults(self):
        pet = Pet("Mochi", "cat")
        task = PetCareTask("Feed Mochi", 15, "high", pet)
        self.assertEqual(task.description, "Feed Mochi")
        self.assertEqual(task.duration, 15)
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.status, "not started")
        self.assertIs(task.pet, pet)
        # default date is today, default start_time is 08:00
        self.assertEqual(task.date, Date.today())
        self.assertEqual(task.start_time, Time(8, 0))

    def test_create_task_explicit_date_time(self):
        pet = Pet("Rex", "dog")
        d = Date(2026, 4, 1)
        t = Time(9, 30)
        task = PetCareTask("Walk Rex", 30, "medium", pet, date=d, start_time=t)
        self.assertEqual(task.date, d)
        self.assertEqual(task.start_time, t)

    def test_task_duration_display(self):
        pet = Pet("Nemo", "fish")
        task = PetCareTask("Clean tank", 90, "low", pet)
        self.assertEqual(task.get_duration_display(), "1h 30m")

    def test_mark_task_done(self):
        pet = Pet("Bella", "dog")
        task = PetCareTask("Grooming", 45, "medium", pet)
        scheduler = Scheduler(Owner("Bob"), 120)
        scheduler.add_task(task)
        scheduler.mark_done(task)
        self.assertEqual(task.status, "done")


# ---------------------------------------------------------------------------
# 2. Schedule respects daily time budget
# ---------------------------------------------------------------------------
class TestSchedulerBudget(unittest.TestCase):

    def _make_tasks(self, specs):
        """specs: list of (description, duration_minutes, time_str 'HH:MM')"""
        pet = Pet("Buddy", "dog")
        d = Date(2026, 4, 1)
        tasks = []
        for desc, dur, t_str in specs:
            h, m = map(int, t_str.split(":"))
            tasks.append(PetCareTask(desc, dur, "medium", pet, date=d, start_time=Time(h, m)))
        return tasks

    def test_all_tasks_fit(self):
        tasks = self._make_tasks([("Feed", 30, "08:00"), ("Walk", 60, "09:00")])
        scheduler = Scheduler(Owner("Alice"), 120)
        for t in tasks:
            scheduler.add_task(t)
        plan = scheduler.generate_plan()
        self.assertEqual(len(plan), 2)

    def test_task_excluded_when_over_budget(self):
        # budget 60 min, three tasks totalling 90 min — last one should be excluded
        tasks = self._make_tasks([
            ("Feed", 30, "08:00"),
            ("Walk", 30, "09:00"),
            ("Bath", 30, "10:00"),
        ])
        scheduler = Scheduler(Owner("Alice"), 60)
        for t in tasks:
            scheduler.add_task(t)
        plan = scheduler.generate_plan()
        self.assertEqual(len(plan), 2)
        descriptions = [t.description for t in plan]
        self.assertNotIn("Bath", descriptions)

    def test_single_task_exactly_fills_budget(self):
        pet = Pet("Mochi", "cat")
        d = Date(2026, 4, 1)
        task = PetCareTask("Long session", 60, "high", pet, date=d, start_time=Time(8, 0))
        scheduler = Scheduler(Owner("Alice"), 60)
        scheduler.add_task(task)
        self.assertEqual(len(scheduler.generate_plan()), 1)

    def test_empty_task_list_returns_empty_plan(self):
        scheduler = Scheduler(Owner("Alice"), 120)
        self.assertEqual(scheduler.generate_plan(), [])

    def test_budget_tracked_per_day(self):
        """Tasks on different days each have their own budget."""
        pet = Pet("Rex", "dog")
        day1 = Date(2026, 4, 1)
        day2 = Date(2026, 4, 2)
        t1 = PetCareTask("Walk day1", 60, "medium", pet, date=day1, start_time=Time(8, 0))
        t2 = PetCareTask("Walk day2", 60, "medium", pet, date=day2, start_time=Time(8, 0))
        scheduler = Scheduler(Owner("Alice"), 60)  # 60 min/day
        scheduler.add_task(t1)
        scheduler.add_task(t2)
        plan = scheduler.generate_plan()
        # Both should fit because they are on different days
        self.assertEqual(len(plan), 2)


# ---------------------------------------------------------------------------
# 3. Tasks are presented in chronological order
# ---------------------------------------------------------------------------
class TestChronologicalOrder(unittest.TestCase):

    def test_same_day_ordered_by_time(self):
        pet = Pet("Buddy", "dog")
        d = Date(2026, 4, 1)
        tasks = [
            PetCareTask("C", 10, "low", pet, date=d, start_time=Time(10, 0)),
            PetCareTask("A", 10, "low", pet, date=d, start_time=Time(8, 0)),
            PetCareTask("B", 10, "low", pet, date=d, start_time=Time(9, 0)),
        ]
        scheduler = Scheduler(Owner("Alice"), 120)
        for t in tasks:
            scheduler.add_task(t)
        plan = scheduler.generate_plan()
        times = [t.start_time for t in plan]
        self.assertEqual(times, sorted(times))

    def test_multi_day_ordered_by_date_then_time(self):
        pet = Pet("Mochi", "cat")
        d1 = Date(2026, 4, 2)
        d2 = Date(2026, 4, 1)
        tasks = [
            PetCareTask("Day2 early", 10, "low", pet, date=d1, start_time=Time(8, 0)),
            PetCareTask("Day1 late",  10, "low", pet, date=d2, start_time=Time(10, 0)),
            PetCareTask("Day1 early", 10, "low", pet, date=d2, start_time=Time(8, 0)),
        ]
        scheduler = Scheduler(Owner("Alice"), 120)
        for t in tasks:
            scheduler.add_task(t)
        plan = scheduler.generate_plan()
        date_times = [(t.date, t.start_time) for t in plan]
        self.assertEqual(date_times, sorted(date_times))


# ---------------------------------------------------------------------------
# 4. Time conflict detection
# ---------------------------------------------------------------------------
class TestConflictDetection(unittest.TestCase):

    def setUp(self):
        self.pet = Pet("Buddy", "dog")
        self.d = Date(2026, 4, 1)
        self.t = Time(9, 0)
        self.existing = [
            PetCareTask("Walk", 30, "medium", self.pet, date=self.d, start_time=self.t)
        ]

    def test_conflict_same_date_and_time(self):
        conflict = has_conflict(self.existing, self.d, self.t)
        self.assertIsNotNone(conflict)
        self.assertEqual(conflict.description, "Walk")

    def test_no_conflict_different_time(self):
        conflict = has_conflict(self.existing, self.d, Time(10, 0))
        self.assertIsNone(conflict)

    def test_no_conflict_different_date(self):
        conflict = has_conflict(self.existing, Date(2026, 4, 2), self.t)
        self.assertIsNone(conflict)

    def test_no_conflict_empty_task_list(self):
        conflict = has_conflict([], self.d, self.t)
        self.assertIsNone(conflict)

    def test_conflict_returns_correct_task_among_many(self):
        extra = PetCareTask("Feed", 15, "high", self.pet, date=self.d, start_time=Time(8, 0))
        tasks = [extra] + self.existing
        conflict = has_conflict(tasks, self.d, self.t)
        self.assertIsNotNone(conflict)
        self.assertEqual(conflict.description, "Walk")


# ---------------------------------------------------------------------------
# INTENTIONALLY FAILING TESTS — expose real gaps in the current implementation
# ---------------------------------------------------------------------------
class TestKnownGaps(unittest.TestCase):

    def test_high_priority_task_not_dropped_when_budget_is_tight(self):
        """
        FAILS: generate_plan() sorts by time only, not priority.
        A low-priority task added early can consume the budget and push out a
        high-priority task added later the same day.

        Expected behaviour: with a 60-min budget, the 'high' priority task
        should always be included even though it starts later.
        Current behaviour: first-in-time wins regardless of priority.
        """
        pet = Pet("Buddy", "dog")
        d = Date(2026, 4, 1)
        low_task  = PetCareTask("Low prio bath",  60, "low",  pet, date=d, start_time=Time(8, 0))
        high_task = PetCareTask("High prio meds", 30, "high", pet, date=d, start_time=Time(9, 0))

        scheduler = Scheduler(Owner("Alice"), 60)
        scheduler.add_task(low_task)
        scheduler.add_task(high_task)

        plan = scheduler.generate_plan()
        descriptions = [t.description for t in plan]

        # This assertion will FAIL — high_task is excluded because low_task
        # consumed the full 60-min budget first.
        self.assertIn("High prio meds", descriptions)

    def test_scheduler_rejects_overlapping_tasks(self):
        """
        FAILS: generate_plan() has no overlap detection.
        Two tasks at the same start time on the same day are both included
        as long as their combined duration fits the budget.

        Expected behaviour: the second task at the same time should be excluded
        (or flagged) because it overlaps with the first.
        Current behaviour: both tasks are included without any conflict check.
        """
        pet = Pet("Mochi", "cat")
        d = Date(2026, 4, 1)
        t1 = PetCareTask("Feed",  30, "high",   pet, date=d, start_time=Time(9, 0))
        t2 = PetCareTask("Brush", 30, "medium", pet, date=d, start_time=Time(9, 0))  # same time!

        scheduler = Scheduler(Owner("Alice"), 120)
        scheduler.add_task(t1)
        scheduler.add_task(t2)

        plan = scheduler.generate_plan()

        # This assertion will FAIL — both tasks land in the plan despite the clash.
        self.assertEqual(len(plan), 1, "Only one task should be scheduled at 9:00 AM")


# ---------------------------------------------------------------------------
# 5. Co-Tasker: acceptance stats and AI task generation (mocked API)
# ---------------------------------------------------------------------------

# Reusable sample suggestions for 2 pets (Buddy the dog, Whiskers the cat)
_SAMPLE_SUGGESTIONS = [
    {"pet_name": "Buddy",    "description": "Feed Buddy",               "duration": 10, "priority": "high", "date": "2026-04-14", "start_time": "08:00"},
    {"pet_name": "Buddy",    "description": "Walk Buddy",                "duration": 30, "priority": "med",  "date": "2026-04-14", "start_time": "09:00"},
    {"pet_name": "Buddy",    "description": "Bathe Buddy",               "duration": 20, "priority": "low",  "date": "2026-04-15", "start_time": "10:00"},
    {"pet_name": "Whiskers", "description": "Feed Whiskers",             "duration": 10, "priority": "high", "date": "2026-04-14", "start_time": "07:00"},
    {"pet_name": "Whiskers", "description": "Scoop Whiskers's Litter Box", "duration": 10, "priority": "high", "date": "2026-04-14", "start_time": "08:30"},
    {"pet_name": "Whiskers", "description": "Brush Whiskers",            "duration": 15, "priority": "low",  "date": "2026-04-15", "start_time": "11:00"},
]


def _acceptance_rate(stats: dict) -> float:
    """Mirror of the acceptance-rate formula used in app.py."""
    total = stats["accepted"] + stats["edited"] + stats["skipped"]
    if total == 0:
        return 0.0
    return (stats["accepted"] + stats["edited"]) / total * 100


class TestCoTaskerStats(unittest.TestCase):
    """Tests for the Co-Tasker acceptance/edit/skip stats tracking."""

    def test_all_accepted_rate_is_100(self):
        stats = {"accepted": 9, "edited": 0, "skipped": 0}
        self.assertEqual(_acceptance_rate(stats), 100.0)

    def test_all_skipped_rate_is_0(self):
        stats = {"accepted": 0, "edited": 0, "skipped": 9}
        self.assertEqual(_acceptance_rate(stats), 0.0)

    def test_edited_tasks_count_as_accepted_in_rate(self):
        # 6 accepted/edited out of 10 total → 60 %
        stats = {"accepted": 4, "edited": 2, "skipped": 4}
        self.assertAlmostEqual(_acceptance_rate(stats), 60.0)

    def test_mixed_accepted_and_edited(self):
        stats = {"accepted": 6, "edited": 2, "skipped": 2}
        self.assertEqual(_acceptance_rate(stats), 80.0)

    def test_empty_stats_returns_zero(self):
        stats = {"accepted": 0, "edited": 0, "skipped": 0}
        self.assertEqual(_acceptance_rate(stats), 0.0)

    def test_only_edited_counts_fully(self):
        stats = {"accepted": 0, "edited": 5, "skipped": 5}
        self.assertEqual(_acceptance_rate(stats), 50.0)


class TestCoTaskerGeneration(unittest.TestCase):
    """Tests for generate_pet_tasks — Gemini API is mocked so no key is needed."""

    def _mock_client(self, suggestions: list):
        """Return a mock Client whose models.generate_content returns suggestions as JSON."""
        mock_response = MagicMock()
        mock_response.text = json.dumps(suggestions)
        mock_client_instance = MagicMock()
        mock_client_instance.models.generate_content.return_value = mock_response
        return mock_client_instance

    @patch("co_tasker.genai.Client")
    def test_returns_three_tasks_per_pet(self, MockClient):
        MockClient.return_value = self._mock_client(_SAMPLE_SUGGESTIONS)
        from co_tasker import generate_pet_tasks
        pets = [Pet("Buddy", "dog"), Pet("Whiskers", "cat")]
        result = generate_pet_tasks(pets, api_key="fake-key")
        self.assertEqual(len(result), 6)  # 3 tasks × 2 pets

    @patch("co_tasker.genai.Client")
    def test_all_pets_represented_in_output(self, MockClient):
        MockClient.return_value = self._mock_client(_SAMPLE_SUGGESTIONS)
        from co_tasker import generate_pet_tasks
        pets = [Pet("Buddy", "dog"), Pet("Whiskers", "cat")]
        result = generate_pet_tasks(pets, api_key="fake-key")
        names_in_result = {t["pet_name"] for t in result}
        self.assertIn("Buddy", names_in_result)
        self.assertIn("Whiskers", names_in_result)

    @patch("co_tasker.genai.Client")
    def test_single_pet_gets_three_tasks(self, MockClient):
        single_pet_suggestions = _SAMPLE_SUGGESTIONS[:3]
        MockClient.return_value = self._mock_client(single_pet_suggestions)
        from co_tasker import generate_pet_tasks
        pets = [Pet("Buddy", "dog")]
        result = generate_pet_tasks(pets, api_key="fake-key")
        self.assertEqual(len(result), 3)

    @patch("co_tasker.genai.Client")
    def test_task_fields_are_present(self, MockClient):
        MockClient.return_value = self._mock_client(_SAMPLE_SUGGESTIONS[:3])
        from co_tasker import generate_pet_tasks
        pets = [Pet("Buddy", "dog")]
        result = generate_pet_tasks(pets, api_key="fake-key")
        required_keys = {"pet_name", "description", "duration", "priority", "date", "start_time"}
        for task in result:
            self.assertTrue(required_keys.issubset(task.keys()), f"Missing keys in: {task}")


if __name__ == "__main__":
    unittest.main()
