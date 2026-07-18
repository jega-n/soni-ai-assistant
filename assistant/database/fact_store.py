from datetime import datetime

from assistant.database.database import Database


class FactStore:

    def __init__(self):

        self.conn = Database.get_connection()
        self._create_table()


    def _create_table(self):

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS facts(

                key TEXT PRIMARY KEY,

                value TEXT NOT NULL,

                updated_at TEXT NOT NULL
            )
        """)

        self.conn.commit()


    def save_fact(
        self,
        key,
        value
    ):

        self.conn.execute(

            """
            INSERT INTO facts(
                key,
                value,
                updated_at
            )
            VALUES (?, ?, ?)

            ON CONFLICT(key)
            DO UPDATE SET

                value = excluded.value,
                updated_at = excluded.updated_at
            """,

            (
                key,
                value,
                datetime.now().isoformat()
            )
        )

        self.conn.commit()


    def get_fact(
        self,
        key
    ):

        row = self.conn.execute(

            """
            SELECT value
            FROM facts
            WHERE key = ?
            """,

            (key,)

        ).fetchone()

        if row:

            return row["value"]

        return None


    def delete_fact(
        self,
        key
    ):

        cursor = self.conn.execute(

            """
            DELETE FROM facts
            WHERE key = ?
            """,

            (key,)
        )

        self.conn.commit()

        return cursor.rowcount > 0


    def list_facts(self):

        rows = self.conn.execute(

            """
            SELECT *
            FROM facts
            ORDER BY key
            """

        ).fetchall()

        return [dict(row) for row in rows]