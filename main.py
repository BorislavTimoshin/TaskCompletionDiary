import csv
import json
import locale
import os
import sys

import pandas as pd
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTableWidgetItem

from src.adding_achievement import AddAchievementToTable
from src.authorization.authorization import Authorization
from src.chart import Chart
from src.user_data_for_chart import UserDataForChart
from src.creating_task import CreateTask
from src.database import db
from src.help import Help
from src.notifications import notifications


if hasattr(Qt, "AA_EnableHighDpiScaling"):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, "AA_UseHighDpiPixmaps"):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


with open("data/translations.json", "r", encoding="utf-8") as json_file:
    translations = json.load(json_file)


class MainWindow(QMainWindow):
    def __init__(self, user_id: int, current_language: str):
        super().__init__()
        uic.loadUi(f"Design/{current_language}/main.ui", self)
        self.user_id = user_id
        self.current_language = current_language
        self.initUI()

    def initUI(self) -> None:
        # MenuBar

        self.download_chart_action.triggered.connect(self.download_chart)
        self.download_table_action.triggered.connect(self.download_table)
        self.show_chart_action.triggered.connect(self.get_user_data_for_chart)
        self.about_action.triggered.connect(self.view_about)
        self.version_action.triggered.connect(self.view_version)
        self.language_english_action.triggered.connect(self.change_language_to_english)
        self.language_russian_action.triggered.connect(self.change_language_to_russian)

        # Push Buttons

        self.btn_create_task.clicked.connect(self.create_task)
        self.btn_add_achievement.clicked.connect(self.add_achievement)
        self.btn_delete_task.clicked.connect(self.delete_task)
        self.btn_delete_achievement.clicked.connect(self.delete_achievement)
        self.btn_logout.clicked.connect(self.logout)

        # Combo Box (Tasks)

        task_names = db.get_task_names(self.user_id)
        self.CB_tasks.addItems(task_names)
        self.CB_tasks.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.CB_tasks.currentTextChanged.connect(self.open_task)

        # Building a table

        self.tableWidget.setColumnWidth(1, 160)

        dateTableWidgetText = translations[self.current_language]["tableWidget"]["date"]
        markTableWidgetText = translations[self.current_language]["tableWidget"]["mark"]
        commentTableWidgetText = translations[self.current_language]["tableWidget"]["comment"]

        current_task = self.CB_tasks.currentText()
        table_result_name = self.get_table_result_name(current_task)

        self.dateTableWidget = QTableWidgetItem(dateTableWidgetText)
        self.resultTableWidget = QTableWidgetItem(table_result_name)
        self.markTableWidget = QTableWidgetItem(markTableWidgetText)
        self.commentTableWidget = QTableWidgetItem(commentTableWidgetText)

        self.tableWidget.setHorizontalHeaderItem(0, self.dateTableWidget)
        self.tableWidget.setHorizontalHeaderItem(1, self.resultTableWidget)
        self.tableWidget.setHorizontalHeaderItem(2, self.markTableWidget)
        self.tableWidget.setHorizontalHeaderItem(3, self.commentTableWidget)

        self.fill_table()

    def change_language_to_english(self) -> None:
        """Translation of the main window text into English"""
        self.current_language = "English"
        uic.loadUi("Design/English/main.ui", self)
        self.initUI()

    def change_language_to_russian(self) -> None:
        """Translation of the main window text into Russian"""
        self.current_language = "Russian"
        uic.loadUi("Design/Russian/main.ui", self)
        self.initUI()

    def fill_table(self) -> None:
        """Filling the table with the user`s achievements for the current sports task"""
        task_name = self.CB_tasks.currentText()
        achievements = db.get_achievements(task_name, self.user_id)
        self.tableWidget.setRowCount(len(achievements))
        for row, (date, result, mark, comment) in enumerate(achievements):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(date.strftime("%d.%m.%Y")))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(result)))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(mark)))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(comment))

    def get_table_result_name(self, task_name: str) -> str:
        """Getting the name of the task result, which is displayed in the table"""
        result_name, unit = db.get_task(task_name, self.user_id)
        if result_name is None and unit is None:
            return translations[self.current_language]["tableWidget"]["defaultResultName"]
        if unit not in ("number", "time"):
            unit_abbr = translations[self.current_language]["unit"][unit]
            return f"{result_name} ({unit_abbr})"
        return result_name

    def open_task(self, task_name: str) -> None:
        """Opening a user`s sport task"""
        table_result_name = self.get_table_result_name(task_name)
        self.resultTableWidget.setText(table_result_name)
        self.fill_table()

    def create_task(self) -> None:
        """Creating a task: task name, result name, unit of measurement"""
        self.creating_task = CreateTask(self, translations)
        self.creating_task.show()

    def delete_task(self) -> None:
        """Deleting a task and everything associated with it"""
        task_name = self.CB_tasks.currentText()
        task_names = db.get_task_names(self.user_id)
        # If there are no tasks, then an error
        if not task_name:
            notifications.cause_error("taskNotCreated", self.current_language)
            return
        should_delete_task = notifications.ask_question(
            self,
            "shouldDeleteTask",
            self.current_language,
        )
        if should_delete_task:
            # Deleting the current task
            self.CB_tasks.removeItem(task_names.index(task_name))
            db.delete_task(task_name, self.user_id)
            # Moving the cursor to the first task and opening it
            self.CB_tasks.setCurrentIndex(0)
            new_task_name = self.CB_tasks.itemText(0)
            self.open_task(new_task_name)

    def add_achievement(self) -> None:
        """Adding an achievement to the table: result date, result, rating, comment"""
        task_name = self.CB_tasks.currentText()
        if not task_name:  # If there are no tasks, then an error
            notifications.cause_error("taskNotCreated", self.current_language)
            return
        self.close()
        self.adding_achievement = AddAchievementToTable(self, translations)
        self.adding_achievement.show()

    def is_table_row_number(self, number: str) -> bool:
        # Checking if the value is an integer
        try:
            row_number = int(number)
        except ValueError:
            notifications.cause_error("isNotInteger", self.current_language)
            return False
        task_name = self.CB_tasks.currentText()
        # Check if a number can be a number in a table
        number_of_achievements = db.get_number_of_achievements(task_name, self.user_id)
        if number_of_achievements < row_number or row_number <= 0:
            notifications.cause_error("lineNumberNotExist", self.current_language)
            return False
        return True

    def delete_achievement(self) -> None:
        """Removing an achievement from the table: result date, result, rating, comment"""
        achievement_number = self.LE_delete_achievement_by_number.text()
        task_name = self.CB_tasks.currentText()
        if self.is_table_row_number(achievement_number):
            achievement_number = int(achievement_number)
            dates = db.get_dates(task_name, self.user_id)
            db.delete_achievement(
                dates[achievement_number - 1],
                task_name,
                self.user_id
            )
            self.LE_delete_achievement_by_number.clear()
            self.fill_table()

    def get_user_data_for_chart(self) -> None:
        self.ex_user_data_for_chart = UserDataForChart(self, translations)
        self.ex_user_data_for_chart.show()
        self.ex_user_data_for_chart.user_data_received.connect(self.show_chart)

    def show_chart(self, data):
        """Demonstration of a graph of the results of the current sports task as a foto"""
        self.ex_chart = Chart(self, data, translations)
        self.ex_chart.show_chart()

    def download_chart(self) -> None:
        """Exporting a graph of the results of the current sports task as a photo"""
        self.ex_chart = UserDataForChart(self, translations)
        self.ex_chart.show()
        data = self.ex_chart.get_user_data_for_chart()
        print(data)
        if self.ex_chart is None:  # For example, an exception occurred
            return
        self.ex_chart.download_chart()

    def download_table(self) -> None:
        """Export table data from an application"""
        task_name = self.CB_tasks.currentText()
        # If there are no tasks, then an error
        if not task_name:
            notifications.cause_error("taskNotCreated", self.current_language)
            return
        file_path, file_type = QFileDialog.getSaveFileName(
            self,
            "Скачать таблицу",
            "",
            "All data(*.xlsx);;CSV data (*.csv)",
        )
        if not file_path:
            return
        csv_path = file_path.replace(".xlsx", ".csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            # Adding Column Titles to a CSV File
            writer.writerow(
                [
                    self.dateTableWidget.text(),
                    self.resultTableWidget.text(),
                    self.markTableWidget.text(),
                    self.commentTableWidget.text(),
                ],
            )
            # Adding achievements to a CSV file
            for row in range(self.tableWidget.rowCount()):
                writer.writerow(
                    [
                        self.tableWidget.item(row, 0).text(),
                        self.tableWidget.item(row, 1).text(),
                        self.tableWidget.item(row, 2).text(),
                        self.tableWidget.item(row, 3).text(),
                    ],
                )
        if file_type == "All data(*.xlsx)":
            # FIXME модифицировать конвертацию
            csv_file = pd.read_csv(csv_path)
            excel_file = pd.ExcelWriter(file_path)
            csv_file.to_excel(excel_file, index=False)
            excel_file._save()
            os.remove(csv_path)

    def view_about(self) -> None:
        """View the program description: how to use the application"""
        self.ex_help = Help(translations, self.current_language)
        self.ex_help.show_about()

    def view_version(self) -> None:
        """View the program version: for developers"""
        self.ex_help = Help(translations, self.current_language)
        self.ex_help.show_version()

    def logout(self) -> None:
        """Logging out of your account (proceeding to authorization)"""
        self.close()
        self.ex_authorization = Authorization(
            main_window=MainWindow,
            translations=translations,
            current_language=self.current_language,
        )
        self.ex_authorization.show()


def get_system_language() -> str:
    """Getting the system language: the language that appears at the beginning of the program
    (for most CIS countries - Russian, otherwise - English)
    P.S. The system language may change as languages are added to the application"""
    language, encoding = locale.getdefaultlocale()
    cis_languages = (
        "ru_RU", "be_BE", "kk_KZ", "uk-UK", "az_AZ", "tk_TM",
        "ky_KG", "ro_MD", "uz_UZ", "hy_AM", "tg_TJ",
    )
    if language in cis_languages:
        return "Russian"
    return "English"


if __name__ == "__main__":
    application = QApplication(sys.argv)
    authorization = Authorization(
        main_window=MainWindow,
        translations=translations,
        current_language=get_system_language(),
    )
    authorization.show()
    sys.exit(application.exec())
