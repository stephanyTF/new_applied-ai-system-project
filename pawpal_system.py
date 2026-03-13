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
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.date, t.start_time))

        daily_used = {}
        plan = []
        for task in sorted_tasks:
            used = daily_used.get(task.date, 0)
            if used + task.duration <= self.time_available:
                plan.append(task)
                daily_used[task.date] = used + task.duration

        return plan
