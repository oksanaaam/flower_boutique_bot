import sqlite3
import unittest
from database.sqlite_db_user import CreateDB


class TestCreateDB(unittest.TestCase):
    def setUp(self):
        self.db_file_name = "test_db.db"
        self.table_name = "test_table"
        self.db = CreateDB(db_file_name=self.db_file_name, tabel_name=self.table_name)

    def tearDown(self):
        # Delete the test database
        try:
            conn = sqlite3.connect(self.db_file_name)
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error in tearDown: {e}")

    def test_set_db(self):
        values = "(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        self.db.set_db(values=values)

        # Check if the table exists
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'"
        )
        table_exists = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table_exists)

    def test_add_db(self):
        values = (1, "John", 30)
        str_v = "(id, name, age)"
        how_many_values = "(?, ?, ?)"
        self.db.set_db(values=str_v)

        self.db.add_db(values=values, str_v=str_v, how_many_values=how_many_values)

        # Check if the row was added
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        result = cursor.fetchone()
        conn.close()

    def test_query_sql(self):
        conn, cursor = self.db.query_sql()

        # Check if the connection and cursor are valid
        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsInstance(cursor, sqlite3.Cursor)
