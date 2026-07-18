from datetime import datetime

from assistant.database.database import Database

class PreferenceStore:

    def __init__(self):

        self.conn = Database.get_connection()
        self._create_table()


    def _create_table(self):

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS preferences(

                key TEXT PRIMARY KEY,

                value TEXT NOT NULL,

                updated_at TEXT NOT NULL
            )
        """)

        self.conn.commit()


    def save_preference(
        self,
        key,
        value
    ):

        self.conn.execute(

            """
            INSERT INTO preferences(
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


    def get_preference(
        self,
        key
    ):

        row = self.conn.execute(

            """
            SELECT value
            FROM preferences
            WHERE key = ?
            """,

            (key,)

        ).fetchone()

        if row:

            return row["value"]

        return None


    def delete_preference(
        self,
        key
    ):

        cursor = self.conn.execute(

            """
            DELETE FROM preferences
            WHERE key = ?
            """,

            (key,)
        )

        self.conn.commit()

        return cursor.rowcount > 0


    def list_preferences(self):

        rows = self.conn.execute(

            """
            SELECT *
            FROM preferences
            ORDER BY key
            """

        ).fetchall()

        return [dict(row) for row in rows]