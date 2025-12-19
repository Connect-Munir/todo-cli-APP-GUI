import unittest
from unittest.mock import MagicMock, patch
from tasks import TaskManager
import io
import sys

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        # Create a mock storage object for each test
        self.mock_storage = MagicMock()
        # Ensure connect() is called when TaskManager is initialized
        self.mock_storage.connect.return_value = None
        self.task_manager = TaskManager(self.mock_storage)

        # Capture print output for assertions
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        # Restore stdout
        sys.stdout = sys.__stdout__

    def test_add_task(self):
        """
        Test that add_task calls storage.execute with the correct parameters.
        """
        self.task_manager.add_task("Test Task", "High")
        self.mock_storage.execute.assert_called_once_with(
            "INSERT INTO tasks (title, priority, done) VALUES (?, ?, ?)", ("Test Task", "High", False)
        )
        self.assertIn("[+] Task added successfully!", self.held_output.getvalue())

    def test_get_tasks_empty(self):
        """
        Test get_tasks when no tasks are found.
        """
        self.mock_storage.fetchall.return_value = []
        tasks = self.task_manager.get_tasks()
        self.mock_storage.fetchall.assert_called_once_with("SELECT id, title, priority, done FROM tasks")
        self.assertEqual(tasks, [])

    def test_get_tasks_with_data(self):
        """
        Test get_tasks when tasks are found.
        """
        mock_tasks = [{"id": 1, "title": "Test Task", "priority": "High", "done": False}]
        self.mock_storage.fetchall.return_value = mock_tasks
        tasks = self.task_manager.get_tasks()
        self.mock_storage.fetchall.assert_called_once_with("SELECT id, title, priority, done FROM tasks")
        self.assertEqual(tasks, mock_tasks)

    def test_list_tasks_with_tasks(self):
        """
        Test that list_tasks displays tasks correctly.
        """
        mock_tasks = [
            {"id": 1, "title": "First Task", "priority": "Low", "done": False},
            {"id": 2, "title": "Second Task Done", "priority": "High", "done": True}
        ]
        self.mock_storage.fetchall.return_value = mock_tasks # This will be called by get_tasks
        self.task_manager.list_tasks()
        output = self.held_output.getvalue()
        self.assertIn("First Task", output)
        self.assertIn("Second Task Done", output)
        self.assertIn("Not Done", output)
        self.assertIn("Done", output)
        self.mock_storage.fetchall.assert_called_once_with("SELECT id, title, priority, done FROM tasks")


    def test_list_tasks_no_tasks(self):
        """
        Test listing tasks when there are none.
        """
        self.mock_storage.fetchall.return_value = [] # This will be called by get_tasks
        self.task_manager.list_tasks()
        self.assertIn("No tasks found.", self.held_output.getvalue())
        self.mock_storage.fetchall.assert_called_once_with("SELECT id, title, priority, done FROM tasks")

    def test_mark_task_found_to_done(self):
        """
        Test marking an undone task as done.
        """
        # Mock _find_task_by_id's behavior through fetchall
        self.mock_storage.fetchall.side_effect = [
            [{"id": 1, "title": "Test Task", "priority": "High", "done": False}], # For _find_task_by_id
            [] # To prevent issues with subsequent fetchall calls if any
        ]
        self.task_manager.mark_task("1")
        self.mock_storage.execute.assert_called_once_with(
            "UPDATE tasks SET done = ? WHERE id = ?", (True, 1)
        )
        self.assertIn("[+] Task status updated.", self.held_output.getvalue())

    def test_mark_task_found_to_undone(self):
        """
        Test marking a done task as undone.
        """
        # Mock _find_task_by_id's behavior through fetchall
        self.mock_storage.fetchall.side_effect = [
            [{"id": 1, "title": "Test Task", "priority": "High", "done": True}], # For _find_task_by_id
            []
        ]
        self.task_manager.mark_task("1")
        self.mock_storage.execute.assert_called_once_with(
            "UPDATE tasks SET done = ? WHERE id = ?", (False, 1)
        )
        self.assertIn("[+] Task status updated.", self.held_output.getvalue())

    def test_mark_task_not_found(self):
        """
        Test marking a task when the task ID doesn't exist.
        """
        self.mock_storage.fetchall.return_value = [] # For _find_task_by_id
        self.task_manager.mark_task("99")
        self.mock_storage.execute.assert_not_called()
        self.assertIn("[!] Task ID not found.", self.held_output.getvalue())
    
    def test_mark_task_invalid_id(self):
        """
        Test marking a task with an invalid (non-numeric) ID.
        """
        self.task_manager.mark_task("abc")
        self.mock_storage.fetchall.assert_not_called() # Corrected: fetchall should not be called for invalid ID
        self.mock_storage.execute.assert_not_called()
        self.assertIn("[!] Task ID not found.", self.held_output.getvalue())


    def test_delete_task_found(self):
        """
        Test deleting a task when the task is found.
        """
        # Mock _find_task_by_id's behavior through fetchall
        self.mock_storage.fetchall.side_effect = [
            [{"id": 1, "title": "Test Task", "priority": "High", "done": False}], # For _find_task_by_id
            []
        ]
        self.task_manager.delete_task("1")
        self.mock_storage.execute.assert_called_once_with(
            "DELETE FROM tasks WHERE id = ?", (1,)
        )
        self.assertIn("[+] Task deleted successfully.", self.held_output.getvalue())

    def test_delete_task_not_found(self):
        """
        Test deleting a task when the task ID doesn't exist.
        """
        self.mock_storage.fetchall.return_value = [] # For _find_task_by_id
        self.task_manager.delete_task("99")
        self.mock_storage.execute.assert_not_called()
        self.assertIn("[!] Task ID not found.", self.held_output.getvalue())
        
    def test_delete_task_invalid_id(self):
        """
        Test deleting a task with an invalid (non-numeric) ID.
        """
        self.task_manager.delete_task("abc")
        self.mock_storage.fetchall.assert_not_called() # Corrected: fetchall should not be called for invalid ID
        self.mock_storage.execute.assert_not_called()
        self.assertIn("[!] Task ID not found.", self.held_output.getvalue())

if __name__ == '__main__':
    unittest.main()