# Python Todo Application

This repository contains a simple yet robust Todo application developed in Python. It offers both a command-line interface (CLI) for quick task management and a graphical user interface (GUI) for a more interactive experience. The application helps users organize their daily tasks efficiently, storing them in a local SQLite database.

## Features

*   **Add Tasks**: Easily add new tasks to your todo list.
*   **View Tasks**: Display all pending and completed tasks.
*   **Mark Tasks as Complete**: Update the status of tasks once finished.
*   **Delete Tasks**: Remove tasks from your list.
*   **Persistent Storage**: All tasks are saved in a `todo.db` SQLite database, ensuring data is retained across sessions.
*   **Dual Interface**: Access the application via a user-friendly CLI or an intuitive GUI.

## Installation

To get started with the Python Todo Application, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/todo-cli.git
    cd todo-cli
    ```
    *(Note: Replace `https://github.com/your-username/todo-cli.git` with your actual repository URL)*

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies**:
    *(Assuming there might be dependencies like `tkinter` for GUI or other modules; if not, this step can be skipped or updated)*
    ```bash
    # If there are any, list them in a requirements.txt file
    # pip install -r requirements.txt
    ```

## Usage

### Command-Line Interface (CLI)

Run the CLI version of the application:

```bash
python main.py
```

Follow the on-screen prompts to manage your tasks.

### Graphical User Interface (GUI)

Run the GUI version of the application:

```bash
python main_gui.py
```

An interactive window will appear, allowing you to manage your tasks visually.

## Project Structure

*   `main.py`: The entry point for the command-line interface.
*   `main_gui.py`: The entry point for the graphical user interface.
*   `tasks.py`: Contains the core logic for managing tasks (adding, deleting, marking complete, etc.).
*   `database.py`: Handles all interactions with the SQLite database (`todo.db`).
*   `todo.db`: The SQLite database file where tasks are stored.
*   `test_tasks.py`: Unit tests for the `tasks.py` module.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is open-source and available under the [MIT License](LICENSE).
*(Note: If you have a different license, please update this section and add a LICENSE file.)*
