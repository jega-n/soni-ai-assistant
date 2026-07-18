from datetime import datetime

from assistant.database.database import Database


class ConversationStore:

    def __init__(self):

        self.conn = Database.get_connection()
        self._create_table()


    def _create_table(self):

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                role TEXT NOT NULL,

                message TEXT NOT NULL,

                timestamp TEXT NOT NULL
            )
        """)

        self.conn.commit()


    def save_message(
        self,
        role,
        message
    ):

        self.conn.execute(

            """
            INSERT INTO conversations(
                role,
                message,
                timestamp
            )
            VALUES (?, ?, ?)
            """,

            (
                role,
                message,
                datetime.now().isoformat()
            )
        )

        self.conn.commit()


    def get_recent_messages(
        self,
        limit=20
    ):

        rows = self.conn.execute(

            """
            SELECT *
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,

            (limit,)

        ).fetchall()

        return [
            dict(row)
            for row in reversed(rows)
        ]


    def clear(self):

        self.conn.execute(
            "DELETE FROM conversations"
        )

        self.conn.commit()