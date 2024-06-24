from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QComboBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QAbstractScrollArea, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QRadioButton, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Py_files.about_program import AboutProgram, get_number_of_records_for_plotting
from Py_files.adding_achievement import AddAchievementToTable
from Py_files.creating_task import CreateTask
from Py_files.warnings import warning_dialog_window
from Py_files.authorization import Authorization
from Py_files.chart import Chart
from Py_files.database import db
from Py_files.colors import *
from typing import Union
import pandas as pd
import csv
import os
import sys

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(550, 200, 800, 700)
        self.setWindowTitle("Дневник выполнения спортивных задач")

        # Icons for actions in the application Toolbar

        self.download_chart_action = QAction(QIcon("Images/chart.png"), "Скачать график", self)
        self.download_table_action = QAction(QIcon("Images/table.png"), "Скачать таблицу", self)
        self.show_chart_action = QAction(QIcon("Images/chart.png"), "Показать график", self)
        self.program_description_action = QAction(QIcon("Images/information.png"), "Описание программы", self)
        self.program_version_action = QAction(QIcon("Images/version.jpg"), "Версия программы", self)

        self.download_chart_action.triggered.connect(self.download_chart)
        self.download_table_action.triggered.connect(self.download_table)
        self.show_chart_action.triggered.connect(self.show_chart)
        self.program_description_action.triggered.connect(self.view_program_description)
        self.program_version_action.triggered.connect(self.view_program_version)

        # The application Toolbar

        self.menu_bar = self.menuBar()

        self.menu_file = self.menu_bar.addMenu("Файл")
        self.menu_file.addAction(self.download_chart_action)
        self.menu_file.addAction(self.download_table_action)

        self.menu_data = self.menu_bar.addMenu("Данные")
        self.menu_data.addAction(self.show_chart_action)

        self.menu_about_program = self.menu_bar.addMenu("О программе")
        self.menu_about_program.addAction(self.program_description_action)
        self.menu_about_program.addAction(self.program_version_action)

        # Buttons:
        # 1) creating a sports task
        # 2) adding an entry to the table

        self.addingDataWidget = QWidget(self)
        self.addingDataWidget.setGeometry(10, 10, 771, 80)

        self.addingDataHLayout = QHBoxLayout(self.addingDataWidget)
        self.addingDataHLayout.setContentsMargins(0, 0, 0, 0)

        self.btn_create_task = QPushButton("Создать задачу", self)
        self.btn_create_task.setGeometry(160, 40, 131, 31)
        self.btn_create_task.clicked.connect(self.create_task)
        self.btn_create_task.setStyleSheet(light_blue_color)
        self.addingDataHLayout.addWidget(self.btn_create_task)

        self.btn_add_achievement = QPushButton("Добавить запись", self)
        self.btn_add_achievement.setGeometry(310, 40, 131, 31)
        self.btn_add_achievement.clicked.connect(self.add_achievement)
        self.btn_add_achievement.setStyleSheet(light_blue_color)
        self.addingDataHLayout.addWidget(self.btn_add_achievement)

        # Opening sport task

        self.lbl_open_task = QLabel(
            "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">"
            "Открыть задачу:</span></p></body></html>",
            self
        )
        self.lbl_open_task.setGeometry(20, 400, 141, 41)

        task_names = db.get_task_names(self.user_id)
        self.CB_tasks = QComboBox(self)
        self.CB_tasks.setGeometry(180, 410, 201, 22)
        self.CB_tasks.addItems(task_names)
        self.CB_tasks.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.CB_tasks.currentTextChanged.connect(self.open_task)

        current_task = self.CB_tasks.currentText()
        result_name, measure = db.get_task(current_task, self.user_id)
        if result_name is None and measure is None:
            result_name = "Результат"
        elif measure not in ["Число", "Время"]:
            result_name = f"{result_name} ({measure})"

        # Plotting chart

        self.lbl_plotting = QLabel(
            "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">"
            "Выберите записи для построения графика:</span></p></body></html>",
            self
        )
        self.lbl_plotting.setGeometry(20, 470, 341, 41)

        self.plotting_option_1 = QRadioButton("Первые 30 записей", self)  # FIXME модифицировать выбор записей
        self.plotting_option_1.setGeometry(20, 520, 141, 21)
        self.plotting_option_1.setChecked(True)

        self.plotting_option_2 = QRadioButton("Первые 60 записей", self)
        self.plotting_option_2.setGeometry(20, 550, 151, 21)

        self.plotting_option_3 = QRadioButton("Первые 90 записей", self)
        self.plotting_option_3.setGeometry(20, 580, 141, 21)

        self.plotting_option_4 = QRadioButton("Первые 120 записей", self)
        self.plotting_option_4.setGeometry(20, 610, 151, 21)

        self.plotting_option_5 = QRadioButton("Первые 150 записей", self)
        self.plotting_option_5.setGeometry(20, 640, 151, 21)

        self.plotting_option_6 = QRadioButton("Первые 180 записей", self)
        self.plotting_option_6.setGeometry(210, 520, 151, 21)

        self.plotting_option_7 = QRadioButton("Первые 270 записей", self)
        self.plotting_option_7.setGeometry(210, 550, 151, 21)

        self.plotting_option_8 = QRadioButton("Первые 365 записей", self)
        self.plotting_option_8.setGeometry(210, 580, 151, 21)

        self.plotting_option_9 = QRadioButton("Первые 730 записей", self)
        self.plotting_option_9.setGeometry(210, 610, 151, 21)

        self.plotting_option_10 = QRadioButton("Все записи", self)
        self.plotting_option_10.setGeometry(210, 640, 101, 21)

        # Building a table

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(10, 75, 771, 301)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setColumnWidth(1, 160)

        self.dateTableWidget = QTableWidgetItem("Дата")
        self.resultTableWidget = QTableWidgetItem(result_name)
        self.markTableWidget = QTableWidgetItem("Оценка \nрезультата")
        self.commentTableWidget = QTableWidgetItem("Комментарий к результату")

        self.tableWidget.setHorizontalHeaderItem(0, self.dateTableWidget)
        self.tableWidget.setHorizontalHeaderItem(1, self.resultTableWidget)
        self.tableWidget.setHorizontalHeaderItem(2, self.markTableWidget)
        self.tableWidget.setHorizontalHeaderItem(3, self.commentTableWidget)

        self.tableWidget.horizontalHeader().setStyleSheet(orange_color)
        self.tableWidget.verticalHeader().setStyleSheet(gray_blue_color)

        self.fill_table()

        # Deleting data

        self.lbl_delete_achievement = QLabel(
            "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">"
            "Удалить запись:</span></p></body></html>",
            self
        )
        self.lbl_delete_achievement.setGeometry(450, 480, 141, 21)

        self.LE_delete_achievement_by_number = QLineEdit(self)
        self.LE_delete_achievement_by_number.setPlaceholderText("Введите номер строки, которую хотите удалить")
        self.LE_delete_achievement_by_number.setGeometry(450, 520, 291, 22)

        self.btn_delete_achievement = QPushButton("Удалить запись", self)
        self.btn_delete_achievement.setGeometry(450, 560, 187, 28)
        self.btn_delete_achievement.clicked.connect(self.delete_achievement)

        self.btn_delete_task = QPushButton("Удалить задачу", self)
        self.btn_delete_task.setGeometry(450, 410, 291, 28)
        self.btn_delete_task.clicked.connect(self.delete_task)

        # Logout from account

        self.btn_logout = QPushButton("Выход", self)
        self.btn_logout.setGeometry(450, 620, 291, 48)
        self.btn_logout.clicked.connect(self.back_to_authorization)
        self.btn_logout.setStyleSheet(light_blue_color)

    def fill_table(self) -> None:
        """ Filling the table with the user's achievements for the current sports task """
        task_name = self.CB_tasks.currentText()
        achievements = db.get_achievements(task_name, self.user_id)
        self.tableWidget.setRowCount(len(achievements))
        for row, (date, result, mark, comment) in enumerate(achievements):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(date.strftime("%d.%m.%Y")))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(result)))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(mark)))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(comment))

    def open_task(self, task_name) -> None:
        """ Opening a user's sport task """
        result_name, measure = db.get_task(task_name, self.user_id)
        # Adding a unit of measurement to the result name (if possible)
        if result_name is None and measure is None:
            result_name = "Результат"
        elif measure not in ["Число", "Время"]:
            result_name = f"{result_name} ({measure})"
        self.resultTableWidget.setText(result_name)
        self.fill_table()
        self.plotting_option_1.setChecked(True)
        self.plotting_option_2.setChecked(False)
        self.plotting_option_3.setChecked(False)
        self.plotting_option_4.setChecked(False)
        self.plotting_option_5.setChecked(False)
        self.plotting_option_6.setChecked(False)
        self.plotting_option_7.setChecked(False)
        self.plotting_option_8.setChecked(False)
        self.plotting_option_9.setChecked(False)
        self.plotting_option_10.setChecked(False)

    def create_task(self) -> None:
        """ Creating a task: task name, result name, unit of measurement """
        self.creating_task = CreateTask(self)
        self.creating_task.show()

    def delete_task(self) -> None:
        """ Deleting a task and everything associated with it """
        task_name = self.CB_tasks.currentText()
        task_names = db.get_task_names(self.user_id)
        # If there are no tasks, then an error
        if not task_name:
            warning_dialog_window.task_not_created()
            return
        answer = warning_dialog_window.delete_task_or_not(self)
        if answer:
            # Deleting the current task
            self.CB_tasks.removeItem(task_names.index(task_name))
            db.delete_task(task_name, self.user_id)
            # Moving the cursor to the first task and opening it
            self.CB_tasks.setCurrentIndex(0)
            new_task_name = self.CB_tasks.itemText(0)
            self.open_task(new_task_name)

    def add_achievement(self) -> None:
        """ Adding an achievement to the table: result date, result, rating, comment """
        task_name = self.CB_tasks.currentText()
        if not task_name:  # If there are no tasks, then an error
            warning_dialog_window.task_not_created()
            return
        self.close()
        self.adding_achievement = AddAchievementToTable(self)
        self.adding_achievement.show()

    def delete_achievement(self) -> None:
        """ Removing an achievement from the table: result date, result, rating, comment """
        achievement_number = self.LE_delete_achievement_by_number.text()
        # Checking if the entered value is an integer
        try:
            achievement_number = int(achievement_number)
        except ValueError:
            warning_dialog_window.is_not_integer()
            return
        task_name = self.CB_tasks.currentText()
        # Checking whether the entered number could be a number in the spreadsheet table
        number_of_achievements = db.get_number_of_achievements(task_name, self.user_id)
        if number_of_achievements < achievement_number or achievement_number <= 0:
            warning_dialog_window.line_number_not_exist()
        else:
            dates = db.get_dates(task_name, self.user_id)
            db.delete_achievement(dates[achievement_number - 1], task_name, self.user_id)
            self.LE_delete_achievement_by_number.clear()
            self.fill_table()

    def get_ex_chart(self) -> Union[Chart, None]:
        """ Getting an exemplar of the Chart class, thanks to which you
        can work with the chart: demonstrate, download, and more """
        current_task = self.CB_tasks.currentText()
        # If there are no tasks, then an error
        if not current_task:
            warning_dialog_window.task_not_created()
            return
        # If there are no achievements, then there is an error
        number_of_achievements = db.get_number_of_achievements(current_task, self.user_id)
        if not number_of_achievements:
            warning_dialog_window.no_achievements_to_plot()
            return
        # We write the name of the result that will be displayed in the graph
        result_name, measure = db.get_task(current_task, self.user_id)
        if measure == "Число":
            pass
        elif measure == "Время":
            result_name = f"{result_name} (с)"
        else:
            result_name = f"{result_name} ({measure})"
        number_of_records_for_plotting = get_number_of_records_for_plotting(self)
        # Getting task results and dates on which they were completed
        results = db.get_results(current_task, self.user_id, sort_by_date_desc=False)
        dates = db.get_dates(current_task, self.user_id, sort_by_date_desc=False)
        points = pd.Series(results, index=dates)
        if number_of_records_for_plotting != "all_records":
            points = pd.Series(results, index=dates)[:number_of_records_for_plotting + 1]
        chart = Chart(points, current_task, result_name, self)
        return chart

    def show_chart(self) -> None:
        """ Demonstration of a graph of the results of the current sports task as a foto """
        self.ex_chart = self.get_ex_chart()
        if self.ex_chart is None:  # For example, an exception occurred
            return
        self.ex_chart.show_chart()

    def download_chart(self) -> None:
        """ Exporting a graph of the results of the current sports task as a photo """
        self.ex_chart = self.get_ex_chart()
        if self.ex_chart is None:  # For example, an exception occurred
            return
        self.ex_chart.download_chart()

    def download_table(self) -> None:
        """ Export table data from an application """
        task_name = self.CB_tasks.currentText()
        # If there are no tasks, then an error
        if not task_name:
            warning_dialog_window.task_not_created()
            return
        file_path, file_type = QFileDialog.getSaveFileName(
            self,
            'Скачать таблицу',
            '',
            'All Other_files(*.xlsx);;CSV Other_files (*.csv)'
        )
        if not file_path:
            return
        csv_path = file_path.replace(".xlsx", ".csv")
        with open(csv_path, 'w', encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            # Adding Column Titles to a CSV File
            writer.writerow([
                self.dateTableWidget.text(),
                self.resultTableWidget.text(),
                self.markTableWidget.text(),
                self.commentTableWidget.text()
            ])
            # Adding achievements to a CSV file
            for row in range(self.tableWidget.rowCount()):
                writer.writerow([
                    self.tableWidget.item(row, 0).text(),
                    self.tableWidget.item(row, 1).text(),
                    self.tableWidget.item(row, 2).text(),
                    self.tableWidget.item(row, 3).text()
                ])
        if file_type == "All Other_files(*.xlsx)":
            # FIXME модифицировать конвертацию
            csv_file = pd.read_csv(csv_path)
            excel_file = pd.ExcelWriter(file_path)
            csv_file.to_excel(excel_file, index=False)
            excel_file._save()
            os.remove(csv_path)

    def view_program_description(self) -> None:
        """ View the program description: how to use the application """
        self.ex_about_program = AboutProgram()
        self.ex_about_program.program_description()

    def view_program_version(self) -> None:
        """ View the program version: for developers """
        self.ex_about_program = AboutProgram()
        self.ex_about_program.program_version()

    def back_to_authorization(self) -> None:
        """ Logging out of your account (proceeding to authorization) """
        self.close()
        self.ex_authorization = Authorization(MainWindow)
        self.ex_authorization.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    authorization = Authorization(MainWindow)
    authorization.show()
    sys.exit(app.exec())
