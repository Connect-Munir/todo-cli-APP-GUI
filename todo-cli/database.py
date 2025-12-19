# database.py
import sqlite3

class Storage:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        """Create a database connection to a SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory = sqlite3.Row
            self.create_table()
        except sqlite3.Error as e:
            print(e)

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def execute(self, sql, params=()):
        """Execute a SQL statement"""
        try:
            c = self.conn.cursor()
            c.execute(sql, params)
            self.conn.commit()
            return c
        except sqlite3.Error as e:
            print(e)
            return None

    def fetchall(self, sql, params=()):
        """Execute a SQL query and fetch all results"""
        try:
            c = self.conn.cursor()
            c.execute(sql, params)
            rows = c.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(e)
            return []

    def create_table(self):
        """Create the tasks table if it doesn't exist"""
        sql = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL,
                done BOOLEAN NOT NULL
            );
        """
        self.execute(sql)

def init_database():
    """Initialize the database and create the table"""
    db = Storage('todo.db')
    db.connect()
    db.create_table()
    db.close()

if __name__ == '__main__':
    init_database()