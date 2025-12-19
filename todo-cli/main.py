# main.py
import sys
from tasks import TaskManager
from database import init_database, Storage
from frontend_gui import TodoApp

G = "\033[92m"
W = "\033[97m"
R = "\033[0m"

class TodoAppCLI:
    def __init__(self):
        storage = Storage('todo.db')
        self.task_manager = TaskManager(storage)

    def run(self):
        while True:
            self.print_menu()
            choice = input(f"\n{W}Choose an option: {R}").strip()
            self.process_choice(choice)

    def print_menu(self):
        print(f"\n{G}==== TODO APP ===={R}")
        print(f"{G}1.{W} Add Task")
        print(f"{G}2.{W} List Tasks")
        print(f"{G}3.{W} Toggle Complete")
        print(f"{G}4.{W} Delete Task")
        print(f"{G}0.{W} Exit{R}")

    def process_choice(self, choice):
        if choice == '1':
            self.add_task()
        elif choice == '2':
            self.list_tasks()
        elif choice == '3':
            self.mark_task()
        elif choice == '4':
            self.delete_task()
        elif choice == '0':
            print(f"{G}Goodbye!{R}")
            exit()
        else:
            print(f"{W}Invalid option.{R}")

    def add_task(self):
        title = input(f"{W}Enter task title: {R}").strip()
        print(f"{G}Priority: (1) Low (2) Medium (3) High{R}")
        p_val = input(f"{W}Select 1-3: {R}").strip()
        p_map = {"1": "Low", "2": "Medium", "3": "High"}
        priority = p_map.get(p_val, "Medium")
        
        if title:
            self.task_manager.add_task(title, priority)

    def list_tasks(self):
        self.task_manager.list_tasks()

    def mark_task(self):
        tid = input(f"{W}Enter ID to toggle: {R}").strip()
        self.task_manager.mark_task(tid)

    def delete_task(self):
        tid = input(f"{W}Enter ID to delete: {R}").strip()
        self.task_manager.delete_task(tid)


if __name__ == "__main__":
    # Initialize database
    init_database()
    
    if "--gui" in sys.argv:
        app = TodoApp()
        app.mainloop()
    else:
        app = TodoAppCLI()
        app.run()