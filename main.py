from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QComboBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QAbstractScrollArea, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QRadioButton, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Py_files.main_buttons import CreateTask, AddAchievementToTable, AboutProgram, get_number_of_records_for_plotting
from Py_files.warnings import warning_dialog_window
from Py_files.authorization import Authorization
from Py_files.chart import Chart
from Py_files.database import db
from Py_files.colors import *
from datetime import datetime
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

    def initUI(self):
        self.setGeometry(550, 200, 800, 700)
        self.setWindowTitle("Дневник выполнения спортивных задач")

        # Icons for actions in the application Toolbar

        self.download_chart_action = QAction(QIcon("Images/chart.png"), "Скачать график", self)
        self.download_table_action = QAction(QIcon("Images/table.png"), "Скачать таблицу", self)
        self.show_chart_action = QAction(QIcon("Images/chart.png"), "Показать график", self)
        self.program_version_action = QAction(QIcon("Images/version.jpg"), "Версия программы", self)

        self.download_chart_action.triggered.connect(self.download_chart)
        self.download_table_action.triggered.connect(self.download_table)
        self.show_chart_action.triggered.connect(self.show_chart)
        self.program_version_action.triggered.connect(self.about_program_dialog)

        # The application Toolbar

        self.menu_bar = self.menuBar()

        self.menu_file = self.menu_bar.addMenu("Файл")
        self.menu_file.addAction(self.download_chart_action)
        self.menu_file.addAction(self.download_table_action)

        self.menu_data = self.menu_bar.addMenu("Данные")
        self.menu_data.addAction(self.show_chart_action)

        self.menu_about_program = self.menu_bar.addMenu("О программе")
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
        self.btn_add_achievement.clicked.connect(self.add_achievement_to_table)
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
        self.tasksCB = QComboBox(self)
        self.tasksCB.setGeometry(180, 410, 201, 22)
        self.tasksCB.addItems(task_names)
        self.tasksCB.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tasksCB.currentTextChanged.connect(self.open_task)

        current_task = self.tasksCB.currentText()
        if current_task:
            result_name, measure = db.get_task(current_task, self.user_id)
            if measure not in ["Число", "Время"]:
                result_name = f"{result_name} ({measure})"
        else:  # Если задание пустое, например при создании самого первого задания
            result_name = ""

        # Plotting chart

        self.lbl_plotting = QLabel(
            "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">"
            "Выберите записи для построения графика:</span></p></body></html>",
            self
        )
        self.lbl_plotting.setGeometry(20, 470, 341, 41)

        self.plotting_option_1 = QRadioButton("Первые 30 записей", self)  # Fixme модифицировать выбор записей
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
            "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">Удалить запись:</span></p></body></html>",
            self
        )
        self.lbl_delete_achievement.setGeometry(450, 480, 141, 21)

        self.delete_achievement_by_numberLE = QLineEdit(self)
        self.delete_achievement_by_numberLE.setPlaceholderText("Введите номер строки, которую хотите удалить")
        self.delete_achievement_by_numberLE.setGeometry(450, 520, 291, 22)

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
        
    def fill_table(self):
        """ Метод заполняющий таблицу данными """
        task_name = self.tasksCB.currentText()
        achievements = db.get_achievements(task_name, self.user_id)
        row = 0
        self.tableWidget.setRowCount(len(achievements))
        for date, result, mark, comment in achievements:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(date))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(result)))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(mark)))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(comment))
            row += 1

    def open_task(self, task_name):
        """ Метод, открывающий выбранное пользователем задание и заполняющий таблицу """
        result_name, measure = db.get_task(task_name, self.user_id)
        if measure not in ["Число", "Время"]:
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

    def download_chart(self, is_show=False):
        current_task = self.tasksCB.currentText()
        result_name, measure = db.get_task(current_task, self.user_id)
        achievements = db.get_achievements(current_task, self.user_id)[::-1]
        dates = list(map(lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"), achievements))
        results = list(map(lambda x: x[1], achievements))
        if measure == "Число":
            result_name = "Результат"
        elif measure == "Время":
            result_name = "Результат (с)"
        else:
            result_name = f"{result_name} ({measure})"
        number_of_records_for_plotting = get_number_of_records_for_plotting(self)
        values = pd.Series(results, index=dates)
        if number_of_records_for_plotting != "all_records":
            values = pd.Series(results, index=dates)[:number_of_records_for_plotting + 1]
        chart = Chart(self, values, result_name)
        if is_show:
            chart.show()
            return
        chart.download_chart()

    def show_chart(self):
        self.download_chart(is_show=True)

    def download_table(self):
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
            writer.writerow([
                self.dateTableWidget.text(),
                self.resultTableWidget.text(),
                self.markTableWidget.text(),
                self.commentTableWidget.text()
            ])
            for i in range(self.tableWidget.rowCount()):
                writer.writerow([
                    self.tableWidget.item(i, 0).text(),
                    self.tableWidget.item(i, 1).text(),
                    self.tableWidget.item(i, 2).text(),
                    self.tableWidget.item(i, 3).text()
                ])
        if file_type == "All Other_files(*.xlsx)":
            csv_file = pd.read_csv(csv_path)
            excel_file = pd.ExcelWriter(file_path)
            csv_file.to_excel(excel_file, index=False)
            excel_file._save()
            os.remove(csv_path)

    def about_program_dialog(self):
        self.about_program = AboutProgram()
        self.about_program.show()

    def create_task(self, is_login_account=False, ex_main_window=None, parent=None, username=None, password=None):
        self.new_task = CreateTask(
            self.tasksCB,
            self.resultTableWidget,
            self.tableWidget,
            self.user_id,
            is_login_account,
            ex_main_window,
            parent,
            username,
            password
        )
        self.new_task.show()

    def add_achievement_to_table(self):
        self.add_achievement = AddAchievementToTable(
            self.tasksCB,
            self.tableWidget,
            self.user_id
        )
        self.add_achievement.show()

    def delete_achievement(self):
        achievement_number = self.delete_achievement_by_numberLE.text()
        try:
            achievement_number = int(achievement_number) - 1
        except ValueError:
            warning_dialog_window.is_not_number()
            return
        task_name = self.tasksCB.currentText()
        achievements = db.get_achievements(task_name, self.user_id)
        if (len(achievements) < (achievement_number + 1)) or achievement_number < 0:
            warning_dialog_window.line_number_not_exist()
        else:
            achievement = achievements[achievement_number]
            del achievements[achievement_number]
            db.delete_achievement(*achievement, task_name, self.user_id)
            # Заполняем таблицу с новыми данными
            row = 0
            self.tableWidget.setRowCount(len(achievements))
            for date, result, mark, comment in achievements:
                self.tableWidget.setItem(row, 0, QTableWidgetItem(date))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(result)))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(mark)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(comment))
                row += 1

    def delete_task(self):
        task_name = self.tasksCB.currentText()
        task_names = db.get_task_names(self.user_id)
        if len(task_names) > 1:  # Если хотя бы одно задание после удаления останется
            answer = warning_dialog_window.delete_task_or_not(self)
            if answer:
                # Удаляем текущее задание
                self.tasksCB.removeItem(task_names.index(task_name))
                db.delete_task(task_name, self.user_id)
                # Переносим курсор на первое задание и открываем его
                self.tasksCB.setCurrentIndex(0)
                new_task_name = self.tasksCB.itemText(0)
                self.open_task(new_task_name)
        else:
            warning_dialog_window.last_task_cannot_be_deleted()

    def back_to_authorization(self):
        self.close()
        self.authorization = Authorization(MainWindow)
        self.authorization.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    authorization = Authorization(MainWindow)
    authorization.show()
    sys.exit(app.exec())
