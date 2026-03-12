from pawpal_system import Pet, Owner, PetCareTask, Scheduler

def main():
    # Create an owner
    owner = Owner("Alice")

    # Create pets
    pet1 = Pet("Lucky", "Dog")
    pet2 = Pet("Junior", "Cat")

    # Add pets to the owner
    owner.pets.append(pet1)
    owner.pets.append(pet2)
    
#"C:\Users\steph\OneDrive\Documents\Code Projects\wk 4 Pet Pals\wk4-pawPal\main.py"
    # Create a scheduler
    scheduler = Scheduler(owner, 180, '2025-03-12')

    # Create pet care tasks
    task1 = PetCareTask("Feed Buddy", 15, "high", pet1)
    task2 = PetCareTask("Walk Buddy", 60, "medium", pet1)
    task3 = PetCareTask("Feed Mittens", 15, "high", pet2)

    # Add tasks to the scheduler
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)

    # Display owner's pets and scheduled tasks
    print(f"{owner.name}'s pets:")
    for pet in owner.pets:
        print(f"- {pet.name} ({pet.type})")

    print("\nScheduled tasks:")
    for task in scheduler.tasks:
        print(f"- {task.description} for {task.get_duration_display()} | ({task.priority}) | Status: {task.status})\n")


if __name__ == "__main__":
    main()