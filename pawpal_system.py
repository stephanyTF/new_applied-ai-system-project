from datetime import date as Date, time as Time


def format_minutes(minutes):
    hours = minutes // 60
    mins = minutes % 60
    if hours and mins:
        return f"{hours}h {mins}m"
    elif hours:
        return f"{hours}h"
    else:
        return f"{mins}m"


class Pet:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []


    def get_name(self):
        return self.name

    def get_pets(self):
        return self.pets

    def get_pet_count(self):
        return len(self.pets)


class PetCareTask:
    def __init__(self, description, duration, priority, pet, date=None, start_time=None):
        self.description = description
        self.duration = duration
        self.priority = priority
        self.status = "not started"
        self.pet = pet
        self.date = date or Date.today()
        self.start_time = start_time or Time(8, 0)

    def set_priority(self, priority):
        self.priority = priority

    def set_status(self, status):
        self.status = status

    def set_duration(self, duration):
        self.duration = duration

    def get_duration_display(self):
        return format_minutes(self.duration)


class Scheduler:
    def __init__(self, owner, time_available, date=None):
        self.owner = owner
        self.time_available = time_available
        self.date = date or Date.today()
        self.tasks = []

    def get_time_available_display(self):
        return format_minutes(self.time_available)

    def add_task(self, task):
        self.tasks.append(task)

    def mark_done(self, task):
        task.set_status("done")

    def generate_plan(self):
        priority_rank = {"high": 0, "med": 1, "low": 2}

        # Group tasks by date
        days = {}
        for task in self.tasks:
            days.setdefault(task.date, []).append(task)

        # Pass 1 — selection: within each day sort by priority then duration (shortest first),
        # greedily fill the daily budget so high-priority tasks are always chosen first
        selected = []
        for day_tasks in days.values():
            day_tasks.sort(key=lambda t: (priority_rank.get(t.priority, 9), t.duration))
            used = 0
            for task in day_tasks:
                if used + task.duration <= self.time_available:
                    selected.append(task)
                    used += task.duration

        # Pass 2 — display: sort selected tasks chronologically by date then start time
        selected.sort(key=lambda t: (t.date, t.start_time))
        return selected
