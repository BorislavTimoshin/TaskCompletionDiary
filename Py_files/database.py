import sqlite3
import datetime


# Класс для работы с базой данных
class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def person_exists(self, username: str, password: str) -> bool:
        with self.connection:
            result = self.cursor.execute(
                "SELECT `username` FROM `Users` WHERE `username` = ? AND `password` = ?",
                (username, password,)
            ).fetchall()
            return bool(result)

    def name_exists(self, username):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `username` FROM `Users` WHERE `username` = ?",
                (username,)
            ).fetchall()
            return bool(result)

    def set_person(self, username, password):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO `Users` (`username`, `password`) VALUES (?, ?)",
                (username, password,)
            )
            self.cursor.execute(
                "INSERT INTO `Tasks` (`id`) VALUES (?)",
                (self.get_id_person(username),)
            )
            self.connection.commit()

    def delete_person(self, id_person):
        with self.connection:
            self.cursor.execute(
                "DELETE FROM `Users` WHERE `id` = ?",
                (id_person,)
            )
            self.cursor.execute(
                "DELETE FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )

    def get_id_person(self, username):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `id` FROM `Users` WHERE `username` = ?",
                (username,)
            ).fetchall()
            for i in result:
                return i[0]

    def set_task_names(self, id_person, task_names):
        self.cursor.execute(
            "UPDATE `Tasks` SET `task_names` = ? WHERE `id` = ?",
            (str(task_names), id_person,)
        )
        self.connection.commit()

    def get_task_names(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `task_names` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            ).fetchall()
            for i in result:
                return eval(i[0])

    def set_result_names(self, id_person, result_names):
        self.cursor.execute(
            "UPDATE `Tasks` SET `result_names` = ? WHERE `id` = ?",
            (str(result_names), id_person,)
        )
        self.connection.commit()

    def get_result_names(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `result_names` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            ).fetchall()
            for i in result:
                return eval(i[0])

    def set_measurements(self, id_person, measurements):
        self.cursor.execute(
            "UPDATE `Tasks` SET `measurements` = ? WHERE `id` = ?",
            (str(measurements), id_person,)
        )
        self.connection.commit()

    def get_measurements(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `measurements` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            ).fetchall()
            for i in result:
                return eval(i[0])

    def set_new_task(self, id_person, task_name, result_name, measurement):
        with self.connection:
            task_names = self.get_task_names(id_person)
            self.cursor.execute(
                "UPDATE `Tasks` SET `task_names` = ? WHERE `id` = ?",
                (str(task_names + [task_name]), id_person,)
            )
            result_names = self.get_result_names(id_person)
            self.cursor.execute(
                "UPDATE `Tasks` SET `result_names` = ? WHERE `id` = ?",
                (str(result_names + [result_name]), id_person,)
            )
            measurements = self.get_measurements(id_person)
            self.cursor.execute(
                "UPDATE `Tasks` SET `measurements` = ? WHERE `id` = ?",
                (str(measurements + [measurement]), id_person,)
            )
            self.connection.commit()

    def get_results(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `results` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )
            for i in result:
                return eval(i[0])

    def set_results(self, id_person, results):
        self.cursor.execute(
            "UPDATE `Tasks` SET `results` = ? WHERE `id` = ?",
            (str(results), id_person,)
        )
        self.connection.commit()

    def get_dates(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `dates` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )
            for i in result:
                return eval(i[0])

    def set_dates(self, id_person, dates):
        self.cursor.execute(
            "UPDATE `Tasks` SET `dates` = ? WHERE `id` = ?",
            (str(dates), id_person,)
        )
        self.connection.commit()

    def get_marks(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `marks` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )
            for i in result:
                return eval(i[0])

    def set_marks(self, id_person, marks):
        self.cursor.execute(
            "UPDATE `Tasks` SET `marks` = ? WHERE `id` = ?",
            (str(marks), id_person,)
        )
        self.connection.commit()

    def get_comments(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `comments` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )
            for i in result:
                return eval(i[0])

    def set_comments(self, id_person, comments):
        self.cursor.execute(
            "UPDATE `Tasks` SET `comments` = ? WHERE `id` = ?",
            (str(comments), id_person,)
        )
        self.connection.commit()


db = Database("Other_files/database.sqlite")  # Экземпляр класса Database для работы с бд
