import datetime
import sqlite3
from typing import Union


class Database:
    def __init__(self, database_path: str):
        self.connection = sqlite3.connect(
            database_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        """Creating database tables if they have not already been created"""
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT,
                    result_name TEXT,
                    unit TEXT,
                    user_id INTEGER
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    result INTEGER,
                    mark INTEGER,
                    comment TEXT,
                    task_id INTEGER
                );
            """)
            self.connection.commit()

    def user_exists(self, login: str, password: str) -> bool:
        """Checking whether a user exists in the database"""
        with self.connection:
            query = """
                SELECT 
                  EXISTS (
                    SELECT 
                      1 
                    FROM 
                      `Users` 
                    WHERE 
                      `login` = ? 
                      AND `password` = ?
                  );
            """
            result = self.cursor.execute(
                query,
                (
                    login,
                    password,
                ),
            ).fetchone()
            return result[0]

    def login_exists(self, login: str) -> bool:
        """Checking if a login exists in the database"""
        with self.connection:
            query = """
                SELECT 
                  EXISTS (
                    SELECT 
                      1 
                    FROM 
                      `Users` 
                    WHERE 
                      `login` = ? 
                  );
            """
            result = self.cursor.execute(query, (login,)).fetchone()
            return result[0]

    def add_user(self, login: str, password: str) -> None:
        """Adding a user to the database"""
        with self.connection:
            query = """ 
                INSERT INTO `Users` (`login`, `password`) 
                VALUES 
                  (?, ?);
            """
            self.cursor.execute(query, (login, password))
            self.connection.commit()

    def get_user_id(self, login: str) -> Union[int, None]:
        with self.connection:
            query = """
                SELECT 
                  `id` 
                FROM 
                  `Users` 
                WHERE 
                  `login` = ?;
            """
            result = self.cursor.execute(query, (login,)).fetchone()
            if result:
                return result[0]
            return None

    def get_number_of_achievements(self, task_name: str, user_id: int) -> int:
        """Getting the number of achievements for a specific sports task"""
        query = """
            SELECT 
              COUNT(*) 
            FROM 
              `Achievements` 
            WHERE 
              `task_id` = ?;
        """
        task_id = self.get_task_id(task_name, user_id)
        result = self.cursor.execute(query, (task_id,)).fetchone()
        if result:
            return result[0]
        return 0

    def add_task(self, task_name: str, result_name: str, unit: str, user_id: int) -> None:
        """Adding task information: task name, task result name, unit of measurement"""
        with self.connection:
            query = """ 
                INSERT INTO `Tasks` (`task_name`, `result_name`, `unit`, `user_id`) 
                VALUES
                  (?, ?, ?, ?);
            """
            self.cursor.execute(
                query,
                (
                    task_name,
                    result_name,
                    unit,
                    user_id,
                ),
            )
            self.connection.commit()

    def get_task(self, task_name: str, user_id: int) -> Union[tuple[str, str], tuple[None, None]]:
        """Getting information about a task: task result name, unit of measurement"""
        with self.connection:
            query = """
                SELECT 
                  result_name,
                  unit
                FROM 
                  `Tasks` 
                WHERE 
                  `task_name` = ? 
                  AND `user_id` = ?;
            """
            result: list[tuple[str, str]] = self.cursor.execute(
                query,
                (
                    task_name,
                    user_id,
                ),
            ).fetchall()
            if result:
                return result[0]
            return None, None

    def get_task_id(self, task_name: str, user_id: int) -> int:
        with self.connection:
            query = """
                SELECT 
                  id 
                FROM 
                  `Tasks` 
                WHERE 
                  `task_name` = ? 
                  AND `user_id` = ?;
            """
            result = self.cursor.execute(
                query,
                (
                    task_name,
                    user_id,
                ),
            ).fetchone()
            return result[0]

    def get_task_names(self, user_id: int) -> list[str]:
        """Getting user task names"""
        with self.connection:
            query = """
                SELECT 
                  task_name 
                FROM 
                  `Tasks` 
                WHERE 
                  `user_id` = ?;
            """
            result: list[tuple[str]] = self.cursor.execute(query, (user_id,)).fetchall()
            return [task_name[0] for task_name in result]

    def delete_task(self, task_name: str, user_id: int) -> None:
        """Removing a user's task from the Tasks table and removing task achievements from the Achievements table"""
        with self.connection:
            query1 = """
                DELETE FROM 
                  `Tasks` 
                WHERE 
                  `id` = ?;
            """
            query2 = """
                DELETE FROM 
                  `Achievements` 
                WHERE 
                  `task_id` = ?;
            """
            task_id = self.get_task_id(task_name, user_id)
            self.cursor.execute(query1, (task_id,))
            self.cursor.execute(query2, (task_id,))

    def add_achievement(
        self, date: datetime.date, result: int, mark: int, comment: str, task_name: str, user_id: int,
    ) -> None:
        """Adding a user achievement for a specific sports task:
        1) date of result
        2) result
        3) rating of your result according to the user from 1 to 5
        4) user comment"""
        with self.connection:
            query = """ 
                INSERT INTO `Achievements` (`date`, `result`, `mark`, `comment`, `task_id`) 
                VALUES
                  (?, ?, ?, ?, ?);
            """
            task_id = self.get_task_id(task_name, user_id)
            self.cursor.execute(
                query,
                (
                    date,
                    result,
                    mark,
                    comment,
                    task_id,
                ),
            )
            self.connection.commit()

    def delete_achievement(self, date: datetime.date, task_name: str, user_id: int) -> None:
        """Deleting a user achievement for a specific sports task"""
        with self.connection:
            query = """
                DELETE FROM
                  `Achievements`
                WHERE
                  `date` = ?
                  AND `task_id` = ?;
            """
            task_id = self.get_task_id(task_name, user_id)
            self.cursor.execute(query, (date, task_id))
            self.connection.commit()

    def get_achievements(
        self, task_name: str, user_id: int, sort_by_date_desc=True,
    ) -> list[tuple[datetime.date, int, int, str]]:
        """Getting all user achievements for a specific sports task"""
        with self.connection:
            if sort_by_date_desc:
                query = """
                    SELECT
                      date,
                      result,
                      mark,
                      comment
                    FROM 
                      `Achievements`
                    WHERE 
                      `task_id` = ?
                    ORDER BY date DESC;
                """
            else:
                query = """
                    SELECT
                      date,
                      result,
                      mark,
                      comment
                    FROM 
                      `Achievements`
                    WHERE 
                      `task_id` = ?
                    ORDER BY date ASC;
                """
            task_id = self.get_task_id(task_name, user_id)
            return self.cursor.execute(query, (task_id,)).fetchall()

    def get_dates(self, task_name: str, user_id: int, sort_by_date_desc=True) -> list[datetime.date]:
        """Getting the dates of the results of a sports task"""
        with self.connection:
            if sort_by_date_desc:
                query = """
                    SELECT
                      date
                    FROM
                      `Achievements`
                    WHERE
                      `task_id` = ?
                    ORDER BY date DESC;
                """
            else:
                query = """
                    SELECT
                      date
                    FROM
                      `Achievements`
                    WHERE
                      `task_id` = ?
                    ORDER BY date ASC;
                """
            task_id = self.get_task_id(task_name, user_id)
            result: list[tuple[datetime.date]] = self.cursor.execute(query, (task_id,)).fetchall()
            return [date[0] for date in result]

    def get_results(self, task_name: str, user_id: int, sort_by_date_desc=True) -> list[int]:
        """Getting of the results of a sports task"""
        with self.connection:
            if sort_by_date_desc:
                query = """
                    SELECT
                      result
                    FROM
                      `Achievements`
                    WHERE
                      `task_id` = ?
                    ORDER BY date DESC;
                """
            else:
                query = """
                    SELECT
                      result
                    FROM
                      `Achievements`
                    WHERE
                      `task_id` = ?
                    ORDER BY date ASC;
                """
            task_id = self.get_task_id(task_name, user_id)
            results: list[tuple[int]] = self.cursor.execute(query, (task_id,)).fetchall()
            return [result[0] for result in results]

    def get_result_name(self, task_name: str, user_id: int) -> Union[str, None]:
        """Getting the name of the result of a specific user's sports task"""
        with self.connection:
            query = """
                SELECT
                  result_name
                FROM 
                  `Tasks`
                WHERE 
                  `id` = ?;
            """
            task_id = self.get_task_id(task_name, user_id)
            result = self.cursor.execute(query, (task_id,)).fetchone()
            if result:
                return result[0]
            return None

    def get_unit(self, task_name: str, user_id: int) -> Union[str, None]:
        """Getting a unit of measurement for the result of a specific sports task of the user"""
        with self.connection:
            query = """
                SELECT
                  unit
                FROM 
                  `Tasks`
                WHERE 
                  `id` = ?;
            """
            task_id = self.get_task_id(task_name, user_id)
            result = self.cursor.execute(query, (task_id,)).fetchone()
            if result:
                return result[0]
            return None


db = Database("data/database.sqlite")
