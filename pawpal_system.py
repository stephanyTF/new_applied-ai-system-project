from datetime import date as Date


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
    def __init__(self, description, duration, priority, pet):
        self.description = description
        self.duration = duration
        self.priority = priority
        self.status = "not started"
        self.pet = pet

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

    def generate_plan(self, sort_by="priority"):
        if sort_by == "duration_asc":
            sorted_tasks = sorted(self.tasks, key=lambda t: t.duration)
        elif sort_by == "duration_desc":
            sorted_tasks = sorted(self.tasks, key=lambda t: t.duration, reverse=True)
        else:
            priority_order = {"high": 0, "med": 1, "low": 2}
            sorted_tasks = sorted(self.tasks, key=lambda t: priority_order.get(t.priority, 3))

        plan = []
        time_remaining = self.time_available
        for task in sorted_tasks:
            if task.duration <= time_remaining:
                plan.append(task)
                time_remaining -= task.duration

        return plan
