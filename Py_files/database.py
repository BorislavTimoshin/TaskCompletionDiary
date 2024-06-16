import sqlite3
import datetime


class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def user_exists(self, name: str, password: str) -> bool:  # FIXME почитать теорию про Exists
        """ Checking whether a user exists in the database """
        with self.connection:
            query = """
                SELECT 
                  `name` 
                FROM 
                  `People` 
                WHERE 
                  `name` = ? 
                  AND `password` = ?;
            """
            result = self.cursor.execute(query, (name, password,)).fetchall()
            return bool(result)

    def name_exists(self, name: str) -> bool:  # FIXME почитать теорию про Exists
        """ Checking if a name exists in the database """
        with self.connection:
            query = """
                SELECT 
                  `name` 
                FROM 
                  `People` 
                WHERE 
                  `name` = ?;
            """
            result = self.cursor.execute(query, (name,)).fetchall()
            return bool(result)

    def add_user(self, name: str, password: str) -> None:
        """ Adding a user to the database """
        with self.connection:
            query = """ 
                INSERT INTO `People` (`name`, `password`) 
                VALUES 
                  (?, ?);
            """
            self.cursor.execute(query, (name, password,))
            self.connection.commit()

    def delete_user(self, user_id: int) -> None:
        """ Removing a user from the database.
         Important: deletion occurs only at the moment the account creation
         is canceled, so the ID is deleted only from the People table """
        with self.connection:
            query = """
                DELETE FROM 
                  `People` 
                WHERE 
                  `id` = ?;
            """
            self.cursor.execute(query, (user_id,))

    def get_user_id(self, name: str) -> int:
        """ Getting user id from database """
        with self.connection:
            query = """
                SELECT 
                  `id` 
                FROM 
                  `People` 
                WHERE 
                  `name` = ?;
            """
            result = self.cursor.execute(query, (name,)).fetchone()
            return result[0]

    def add_task(self, task_name, result_name, measure, user_id):
        """ Adding task information: task name, task result name, unit of measurement """
        with self.connection:
            query = """ 
                INSERT INTO `Tasks` (`task_name`, `result_name`, `measure`, `id`) 
                VALUES
                  (?, ?, ?, ?);
            """
            self.cursor.execute(query, (task_name, result_name, measure, user_id,))
            self.connection.commit()

    def get_task(self, task_name: str, user_id: int) -> tuple[str]:
        with self.connection:
            query = """
                SELECT 
                  result_name,
                  measure
                FROM 
                  `Tasks` 
                WHERE 
                  `task_name` = ? 
                  AND `id` = ?;
            """
            result = self.cursor.execute(query, (task_name, user_id,)).fetchall()
            return result[0]

    def get_task_id(self, task_name: str, user_id: int) -> int:
        with self.connection:
            query = """
                SELECT 
                  task_id 
                FROM 
                  `Tasks` 
                WHERE 
                  `task_name` = ? 
                  AND `id` = ?;
            """
            result = self.cursor.execute(query, (task_name, user_id,)).fetchone()
            return result[0]

    def get_task_names(self, user_id: int) -> list[str]:
        with self.connection:
            query = """
                SELECT 
                  task_name 
                FROM 
                  `Tasks` 
                WHERE 
                  `id` = ?;
            """
            result = self.cursor.execute(query, (user_id,)).fetchall()
            task_names = list(map(lambda x: x[0], result))
            return task_names

    def get_task_ids(self, user_id: int) -> list[int]:
        """ Retrieving IDs of all user tasks """
        with self.connection:
            query = """
                SELECT 
                  task_id 
                FROM 
                  `Tasks` 
                WHERE 
                  `id` = ?;
            """
            result = self.cursor.execute(query, (user_id,)).fetchall()
            task_ids = list(map(lambda x: x[0], result))
            return task_ids

    def delete_task(self, task_name, user_id):
        with self.connection:
            query1 = """
                DELETE FROM 
                  `Tasks` 
                WHERE 
                  `task_id` = ?;
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

    def add_achievement(self, date: datetime.datetime, result: int, mark: int, comment: str, task_name: str, user_id: int) -> None:
        with self.connection:
            query = """ 
                INSERT INTO `Achievements` (`date`, `result`, `mark`, `comment`, `task_id`) 
                VALUES
                  (?, ?, ?, ?, ?)
            """
            task_id = self.get_task_id(task_name, user_id)
            self.cursor.execute(query, (date, result, mark, comment, task_id,))
            self.connection.commit()

    def delete_achievement(self, date: datetime.datetime, result: int, mark: int, comment: str, task_name: str, user_id: int) -> None:
        with self.connection:
            query = """
                DELETE FROM
                  `Achievements`
                WHERE
                  `date` = ?
                  AND `result` = ?
                  AND `mark` = ?
                  AND `comment` = ?
                  AND `task_id` = ?
            """
            task_id = self.get_task_id(task_name, user_id)
            self.cursor.execute(query, (date, result, mark, comment, task_id))
            self.connection.commit()

    def get_achievements(self, task_name: str, user_id: int) -> list[tuple[datetime.datetime, int, int, str]]:
        with self.connection:
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
            task_id = self.get_task_id(task_name, user_id)
            result = self.cursor.execute(query, (task_id,)).fetchall()
            return result

    def get_measure(self, task_name: str, user_id: int) -> str:
        with self.connection:
            query = """
                SELECT
                  measure
                FROM 
                  `Tasks`
                WHERE 
                  `task_id` = ?
            """
            task_id = self.get_task_id(task_name, user_id)
            result = self.cursor.execute(query, (task_id,)).fetchone()
            return result[0]

    def get_result_name(self, task_name: str, user_id: int) -> str:
        with self.connection:
            query = """
                SELECT
                  result_name
                FROM 
                  `Tasks`
                WHERE 
                  `task_id` = ?
            """
            task_id = self.get_task_id(task_name, user_id)
            result = self.cursor.execute(query, (task_id,)).fetchone()
            return result[0]


db = Database("Other_files/database.sqlite")
