import os
import json

# File paths
TASKS_FILE = 'tasks.txt'
BACKUP_FILE = 'tasks_backup.txt'

# Load tasks from file
if os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'r') as file:
        tasks = json.load(file)
else:
    tasks = []

# Function to save tasks to file
def save_tasks():
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

# Function to backup tasks before exiting
def backup_tasks():
    with open(BACKUP_FILE, 'w') as file:
        json.dump(tasks, file)

# Main loop
while True:
    print("\n1. Add Task\n2. Mark Task as Completed\n3. Delete Task\n4. View Pending Tasks\n5. View Completed Tasks\n6. Exit")
    choice = input("Choose an option: ")
    
    if choice == '1':  # Add Task
        task_description = input("Enter task description: ")
        priority = input("Enter priority (High/Medium/Low): ").capitalize()
        
        # Simple validation for priority
        if priority not in ['High', 'Medium', 'Low']:
            print("Invalid priority! Please enter High, Medium, or Low.")
            continue

        task = {
            'description': task_description,
            'priority': priority,
            'completed': False
        }
        tasks.append(task)
        save_tasks()
        print("Task added.")

    elif choice == '2':  # Mark Task as Completed
        task_to_complete = input("Enter the description of the task to mark as completed: ")
        for task in tasks:
            if task['description'] == task_to_complete and not task['completed']:
                task['completed'] = True
                save_tasks()
                print("Task marked as completed.")
                break
        else:
            print("Task not found or already completed.")

    elif choice == '3':  # Delete Task
        task_to_delete = input("Enter the description of the task to delete: ")
        for i, task in enumerate(tasks):
            if task['description'] == task_to_delete:
                del tasks[i]
                save_tasks()
                print("Task deleted.")
                break
        else:
            print("Task not found.")

    elif choice == '4':  # View Pending Tasks
        print("Pending Tasks:")
        pending_tasks = [task for task in tasks if not task['completed']]
        if not pending_tasks:
            print("No pending tasks.")
        else:
            for task in pending_tasks:
                print(f"{task['description']} - Priority: {task['priority']}")

    elif choice == '5':  # View Completed Tasks
        print("Completed Tasks:")
        completed_tasks = [task for task in tasks if task['completed']]
        if not completed_tasks:
            print("No completed tasks.")
        else:
            for task in completed_tasks:
                print(f"{task['description']} - Priority: {task['priority']}")

    elif choice == '6':  # Exit
        backup_tasks()
        print("Backup created. Exiting the program.")
        break

    else:
        print("Invalid option! Please try again.")