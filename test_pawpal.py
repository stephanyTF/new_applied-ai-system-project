import unittest
from datetime import date as Date, time as Time

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


if __name__ == "__main__":
    unittest.main()
