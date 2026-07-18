from datetime import datetime

from assistant.database.database import Database


class TaskStore:

    def __init__(self):

        self.conn = Database.get_connection()
        self._create_table()


    def _create_table(self):

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                type TEXT NOT NULL,

                title TEXT NOT NULL,

                time TEXT,

                status TEXT NOT NULL,

                created_at TEXT NOT NULL
            )
        """)

        self.conn.commit()


    def create_task(
        self,
        task_type,
        title,
        time=None
    ):

        cursor = self.conn.execute(

            """
            INSERT INTO tasks
            (
                type,
                title,
                time,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,

            (
                task_type,
                title,
                time,
                "pending",
                datetime.now().isoformat()
            )
        )

        self.conn.commit()

        return cursor.lastrowid


    def list_tasks(self):

        rows = self.conn.execute(

            """
            SELECT *
            FROM tasks
            ORDER BY id
            """

        ).fetchall()

        return [dict(row) for row in rows]


    def delete_task(
        self,
        task_id
    ):

        cursor = self.conn.execute(

            """
            DELETE FROM tasks
            WHERE id = ?
            """,

            (task_id,)
        )

        self.conn.commit()

        return cursor.rowcount > 0


    def update_status(
        self,
        task_id,
        status
    ):

        cursor = self.conn.execute(

            """
            UPDATE tasks
            SET status = ?
            WHERE id = ?
            """,

            (
                status,
                task_id
            )
        )

        self.conn.commit()

        return cursor.rowcount > 0