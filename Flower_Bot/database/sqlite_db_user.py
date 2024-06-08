import sqlite3
from typing import Any

from aiogram import types
from loader import dp


class CreateDB:
    def __init__(self, *, db_file_name: str, tabel_name: str):
        self.db_file_name = db_file_name
        self.table_name = tabel_name

    def set_db(self, *, values: str) -> None:
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} {values}
    """
        )
        conn.commit()
        conn.close()

    async def add_db(
        self, *, values: tuple[Any, Any, str], str_v: str, how_many_values: str
    ) -> None:
        base = sqlite3.connect(self.db_file_name)
        cursor = base.cursor()
        cursor.execute(
            f"""INSERT INTO {self.table_name} {str_v}
                                            VALUES {how_many_values}""",
            values,
        )
        base.commit()
        base.close()

    def query_sql(self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()
        return conn, cursor
