import tkinter as tk
from tkinter import ttk, messagebox
from tasks import TaskManager
from database import Storage, init_database

class TodoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Todo App")
        master.geometry("800x600")
        master.resizable(False, False)

        # Initialize TaskManager
        self.storage = Storage('todo.db')
        self.storage.connect()
        self.task_manager = TaskManager(self.storage)

        # --- Styling ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # Use a modern theme

        # Configure colors for a professional look
        self.primary_color = "#4CAF50" # Green
        self.secondary_color = "#3E8E41" # Darker Green
        self.accent_color = "#FFC107" # Amber
        self.bg_color = "#E0E0E0" # Light Gray
        self.fg_color = "#333333" # Dark Gray
        self.done_color = "#A5D6A7" # Light Green for done tasks
        self.not_done_color = "#EF9A9A" # Light Red for not done tasks

        master.configure(bg=self.bg_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color, font=('Helvetica', 10))
        self.style.configure('TButton', background=self.primary_color, foreground='white', font=('Helvetica', 10, 'bold'))
        self.style.map('TButton', background=[('active', self.secondary_color)])
        self.style.configure('TEntry', fieldbackground='white', foreground=self.fg_color)
        self.style.configure('TCombobox', fieldbackground='white', foreground=self.fg_color)
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'), background=self.primary_color, foreground='white')
        self.style.configure('Treeview', background='white', foreground=self.fg_color, fieldbackground='white', font=('Helvetica', 10))
        self.style.map('Treeview', background=[('selected', self.accent_color)], foreground=[('selected', 'black')])


        # --- Input Frame ---
        input_frame = ttk.Frame(master, padding="15")
        input_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(input_frame, text="Task Title:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.task_title_entry = ttk.Entry(input_frame, width=40)
        self.task_title_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(input_frame, text="Priority:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.priority_combobox = ttk.Combobox(input_frame, values=["Low", "Medium", "High"], state="readonly")
        self.priority_combobox.set("Medium")
        self.priority_combobox.grid(row=1, column=1, sticky="w", pady=5, padx=5)

        add_button = ttk.Button(input_frame, text="Add Task", command=self.add_task_gui)
        add_button.grid(row=0, column=2, rowspan=2, padx=10, sticky="ns")

        # --- Task List Frame ---
        task_list_frame = ttk.Frame(master, padding="15")
        task_list_frame.pack(pady=5, padx=10, fill="both", expand=True)

        self.task_tree = ttk.Treeview(task_list_frame, columns=("ID", "Title", "Priority", "Status"), show="headings")
        self.task_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.task_tree.heading("Title", text="Title", anchor=tk.W)
        self.task_tree.heading("Priority", text="Priority", anchor=tk.CENTER)
        self.task_tree.heading("Status", text="Status", anchor=tk.CENTER)

        self.task_tree.column("ID", width=50, stretch=tk.NO, anchor=tk.CENTER)
        self.task_tree.column("Title", width=350, stretch=tk.YES)
        self.task_tree.column("Priority", width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.task_tree.column("Status", width=100, stretch=tk.NO, anchor=tk.CENTER)

        self.task_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(task_list_frame, orient="vertical", command=self.task_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        self.task_tree.tag_configure('done', background=self.done_color)
        self.task_tree.tag_configure('not_done', background=self.not_done_color)

        # --- Action Buttons Frame ---
        action_button_frame = ttk.Frame(master, padding="15")
        action_button_frame.pack(pady=10, padx=10, fill="x")

        toggle_button = ttk.Button(action_button_frame, text="Toggle Status", command=self.toggle_task_status)
        toggle_button.pack(side="left", padx=5, expand=True)

        delete_button = ttk.Button(action_button_frame, text="Delete Task", command=self.delete_task_gui)
        delete_button.pack(side="left", padx=5, expand=True)

        refresh_button = ttk.Button(action_button_frame, text="Refresh List", command=self.refresh_task_list)
        refresh_button.pack(side="left", padx=5, expand=True)

        # Initial load
        self.refresh_task_list()

    def add_task_gui(self):
        title = self.task_title_entry.get().strip()
        priority = self.priority_combobox.get()
        if not title:
            messagebox.showwarning("Input Error", "Task title cannot be empty.")
            return
        
        self.task_manager.add_task(title, priority)
        self.task_title_entry.delete(0, tk.END)
        self.refresh_task_list()
        messagebox.showinfo("Success", "Task added successfully!")

    def refresh_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        tasks = self.task_manager.get_tasks()
        for task in tasks:
            status = "Done" if task["done"] else "Not Done"
            tag = 'done' if task["done"] else 'not_done'
            self.task_tree.insert("", "end", values=(task["id"], task["title"], task["priority"], status), tags=(tag,))

    def get_selected_task_id(self):
        selected_item = self.task_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task from the list.")
            return None
        
        task_id = self.task_tree.item(selected_item, "values")[0]
        return task_id

    def toggle_task_status(self):
        task_id = self.get_selected_task_id()
        if task_id is not None:
            self.task_manager.mark_task(task_id)
            self.refresh_task_list()
            messagebox.showinfo("Success", f"Task {task_id} status toggled.")

    def delete_task_gui(self):
        task_id = self.get_selected_task_id()
        if task_id is not None:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Task ID {task_id}?"):
                self.task_manager.delete_task(task_id)
                self.refresh_task_list()
                messagebox.showinfo("Success", f"Task {task_id} deleted.")

def main_gui():
    init_database() # Ensure database is initialized
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main_gui()