import customtkinter as ctk
import database
import tasks  # Importing your database logic

# Set the appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db_storage = database.Storage('todo.db')
        self.db_storage.connect()
        self.task_manager = tasks.TaskManager(self.db_storage)

        self.title("AI-101 Python Todo - Frontend")
        self.geometry("600x500")

        # --- UI Layout ---
        self.label = ctk.CTkLabel(self, text="MY TODO LIST", font=("Arial", 24, "bold"), text_color="#2ecc71")
        self.label.pack(pady=20)

        # Input Frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter task title...")
        self.task_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        self.priority_dropdown = ctk.CTkComboBox(self.input_frame, values=["Low", "Medium", "High"])
        self.priority_dropdown.set("Medium")
        self.priority_dropdown.pack(side="left", padx=10)

        self.add_button = ctk.CTkButton(self.input_frame, text="Add Task", command=self.add_task_ui)
        self.add_button.pack(side="left", padx=10)

        # Scrollable Task List
        self.task_list_frame = ctk.CTkScrollableFrame(self, label_text="Tasks")
        self.task_list_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.load_tasks_ui()

    def load_tasks_ui(self):
        """Clears and reloads tasks from the database into the UI."""
        # Clear existing widgets in the scrollable frame
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        # Fetch from DB using TaskManager
        tasks_data = self.task_manager.get_tasks()

        for task in tasks_data:
            task_id, title, priority, done = task['id'], task['title'], task['priority'], task['done']
            status_text = "Done" if done else "Not Done"
            btn_color = "#27ae60" if done else "#34495e"

            # Create a row frame for each task
            row_frame = ctk.CTkFrame(self.task_list_frame)
            row_frame.pack(fill="x", pady=5)

            lbl = ctk.CTkLabel(row_frame, text=f"ID: {task_id} [{priority}] {title}", width=300, anchor="w")
            lbl.pack(side="left", padx=10)

            # Toggle Status Button
            done_btn = ctk.CTkButton(row_frame, text=status_text, width=80, fg_color=btn_color,
                                     command=lambda i=task_id: self.toggle_task_ui(i))
            done_btn.pack(side="right", padx=5)

            # Delete Button
            del_btn = ctk.CTkButton(row_frame, text="Delete", width=80, fg_color="#c0392b",
                                    command=lambda i=task_id: self.delete_task_ui(i))
            del_btn.pack(side="right", padx=5)

    def add_task_ui(self):
        title = self.task_entry.get()
        priority = self.priority_dropdown.get()
        if title:
            self.task_manager.add_task(title, priority)
            self.task_entry.delete(0, 'end')
            self.load_tasks_ui()

    def toggle_task_ui(self, task_id):
        self.task_manager.mark_task(task_id)
        self.load_tasks_ui()

    def delete_task_ui(self, task_id):
        self.task_manager.delete_task(task_id)
        self.load_tasks_ui()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()