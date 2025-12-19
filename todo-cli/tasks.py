# tasks.py
# ANSI Color Codes
G = "\033[92m"  # Green
W = "\033[97m"  # White
R = "\033[0m"   # Reset
RR = "\033[91m"  # Red

class TaskManager:
    def __init__(self, storage):
        self.db = storage
        self.db.connect()

    def _find_task_by_id(self, task_id_input):
        """Helper to find a task dictionary by its ID."""
        try:
            t_id = int(task_id_input)
            tasks = self.db.fetchall("SELECT id, title, priority, done FROM tasks WHERE id = ?", (t_id,))
            if tasks:
                return tasks[0]
        except ValueError:
            pass
        return None

    def add_task(self, title, priority):
        """Adds a task with priority to the list."""
        self.db.execute("INSERT INTO tasks (title, priority, done) VALUES (?, ?, ?)", (title, priority, False))
        print(f"{G}[+] Task added successfully!{R}")

    def get_tasks(self):
        """Fetches all tasks from the database."""
        return self.db.fetchall("SELECT id, title, priority, done FROM tasks")

    def list_tasks(self):
        """Displays tasks in a formatted table."""
        tasks = self.get_tasks()
        if not tasks:
            print(f"\n{W}[!] No tasks found.{R}")
            return

        # Determine column widths dynamically
        max_title = max(len(t["title"]) for t in tasks) if tasks else 25
        id_width = 4
        title_width = max(max_title, len("Task Title")) + 2
        priority_width = 12
        status_width = 12

        # Header
        header = (
            f"{G}{'ID':<{id_width}} | "
            f"{ 'Task Title':<{title_width}} | "
            f"{ 'Priority':<{priority_width}} | "
            f"{ 'Status':<{status_width}}{R}"
        )
        divider = f"{W}{'-' * (id_width + title_width + priority_width + status_width + 9)}{R}"

        print("\n" + header)
        print(divider)

        # Task Rows
        for task in tasks:
            status = "Done" if task["done"] else "Not Done"
            s_color = G if task["done"] else RR  # Green for Done, Red for Not Done

            print(
                f"{W}{task['id']:<{id_width}}{R} | "
                f"{W}{task['title']:<{title_width}}{R} | "
                f"{W}{task['priority']:<{priority_width}}{R} | "
                f"{s_color}{status:<{status_width}}{R}"
            )
        print(divider)

    def mark_task(self, task_id):
        """Flips completion status."""
        task = self._find_task_by_id(task_id)
        if task:
            self.db.execute("UPDATE tasks SET done = ? WHERE id = ?", (not task['done'], task['id']))
            print(f"{G}[+] Task status updated.{R}")
        else:
            print(f"{W}[!] Task ID not found.{R}")

    def delete_task(self, task_id):
        """Removes task from list."""
        task = self._find_task_by_id(task_id)
        if task:
            self.db.execute("DELETE FROM tasks WHERE id = ?", (task['id'],))
            print(f"{G}[+] Task deleted successfully.{R}")
        else:
            print(f"{W}[!] Task ID not found.{R}")
