# To-do list
tasks = [] 

def show_tasks():
    """Displays all tasks with their status."""
    if not tasks:
        print("No tasks yet, my dude! Time to add some.")
        return
    
    print("\n Your Current Tasks my bro:")
 
    for i, t in enumerate(tasks, 1):
        
        status = "[DONE]" if t['done'] else "[TODO]"
        print(f"**{i}. {status}** {t['name']}")
    print("-" * 25)

def add_task():
    """Prompts for a new task and adds it to the list my dude."""
    task_name = input("New task my guy: ").strip()
    if task_name:
        
        tasks.append({'name': task_name, 'done': False})
        print(f"'{task_name}' added to the list!")
    else:
        print("Task cannot be empty, my bro.")

def remove_task():
    """Removes a task by its number."""
    if not tasks:
        print("Nothing to remove, my dude.")
        return
        
    show_tasks() 
    
    try:
        idx = int(input("Remove task # my guy: "))
        
        if 1 <= idx <= len(tasks):
            removed_task = tasks.pop(idx - 1)
            print(f"Task #{idx} - '{removed_task['name']}' has been removed!")
        else:
            print(f"Invalid number. Please enter a number between 1 and {len(tasks)}.")
    except ValueError:
        print("Invalid input! Please enter a number.")

def mark_done():
    """Marks a task as complete by its number."""
    if not tasks:
        print("Nothing to mark as done, my dude.")
        return
    
    show_tasks()
    
    try:
        idx = int(input("Mark task # as DONE: "))
        if 1 <= idx <= len(tasks):
            tasks[idx - 1]['done'] = True
            print(f"Task #{idx} - '{tasks[idx - 1]['name']}' marked as DONE!")
        else:
            print(f"Invalid number. Please enter a number between 1 and {len(tasks)}.")
    except ValueError:
        print("Invalid input! Please enter a number bro.")




while True:
    print("\n--- To Do List Menu ---")
    print("1. Show Tasks")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Mark Task as Done (NEW!)")
    print("5. Exit")
    
    choice = input("Choose my dude (1-5): ")
    
    if choice == "1":
        show_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        remove_task()
    elif choice == "4":
        mark_done()
    elif choice == "5":
        print("Catch you later! Your to-do list is safe...or is it.....")
        break
    else:
        print("Invalid choice my bro! Please choose a number from 1 to 5.")