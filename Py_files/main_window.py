from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QComboBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QAbstractScrollArea, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Py_files.main_buttons import CreateTask, AddEntry, AboutProgram, get_number_of_records_for_plotting
from Py_files.warnings_dialog_window import warning_dialog_window
from Py_files.chart import Chart
from Py_files.database import db
import pandas as pd
import csv
import os


# Класс с главным окном для работы с аккаунтом пользователя
class MainWindow(QMainWindow):
    def __init__(self, id_person, dad=None):
        super().__init__()
        self.id_person = id_person
        self.dad = dad
        self.initUI()

    def initUI(self):
        self.setGeometry(550, 200, 800, 700)
        self.setWindowTitle("Дневник выполнения спортивных задач")

        self.download_chart_action = QAction(QIcon("Images/chart.png"), "Скачать график", self)
        self.download_table_action = QAction(QIcon("Images/table.png"), "Скачать таблицу", self)
        self.show_chart_action = QAction(QIcon("Images/chart.png"), "Показать график", self)
        self.program_version_action = QAction(QIcon("Images/version.jpg"), "Версия программы", self)

        self.download_chart_action.triggered.connect(self.download_chart)
        self.download_table_action.triggered.connect(self.download_table)
        self.show_chart_action.triggered.connect(self.show_chart)
        self.program_version_action.triggered.connect(self.about_program_dialog)

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Файл")
        self.data_menu = self.menu.addMenu("Данные")
        self.about_program_menu = self.menu.addMenu("О программе")

        self.file_menu.addAction(self.download_chart_action)
        self.file_menu.addAction(self.download_table_action)
        self.data_menu.addAction(self.show_chart_action)
        self.about_program_menu.addAction(self.program_version_action)

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(10, 10, 771, 80)
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.btn_create_task = QPushButton("Создать задачу", self.horizontalLayoutWidget)
        self.btn_create_task.setGeometry(160, 40, 131, 31)
        self.horizontalLayout.addWidget(self.btn_create_task)
        self.btn_create_task.clicked.connect(self.create_new_task)

        self.btn_new_entry = QPushButton("Добавить запись", self.horizontalLayoutWidget)
        self.btn_new_entry.setGeometry(310, 40, 131, 31)
        self.horizontalLayout.addWidget(self.btn_new_entry)
        self.btn_new_entry.clicked.connect(self.add_entry_to_table)

        light_blue_color = "QPushButton""{""background-color : lightblue;""}"
        self.btn_create_task.setStyleSheet(light_blue_color)
        self.btn_new_entry.setStyleSheet(light_blue_color)

        self.lbl_open_task = QLabel("<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">"
                                    "Открыть задачу:</span></p></body></html>", self)
        self.lbl_open_task.setGeometry(20, 400, 141, 41)

        self.plotting = QLabel("<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">"
                               "Выберите записи для построения графика:</span></p></body></html>", self)
        self.plotting.setGeometry(20, 470, 341, 41)

        self.plotting_option_1 = QRadioButton("Первые 30 записей", self)
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

        task_names = db.get_task_names(self.id_person)
        result_names = db.get_result_names(self.id_person)
        measurements = db.get_measurements(self.id_person)

        self.btn_open_task = QComboBox(self)
        self.btn_open_task.setGeometry(180, 410, 201, 22)
        self.btn_open_task.addItems(task_names)
        self.btn_open_task.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.btn_open_task.view().pressed.connect(self.open_task)
        current_task = self.btn_open_task.currentText()
        if current_task:
            index_current_task = task_names.index(current_task)
            result_value = result_names[index_current_task]
            measurement = measurements[index_current_task]
            if measurement not in ["Число", "Время"]:
                result_value = f"{result_value} ({measurement})"
        else:
            result_value = ""

        self.table = QTableWidget(self)
        self.table.setGeometry(10, 75, 771, 301)
        self.table.setColumnCount(4)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(1, 160)

        self.date_value = QTableWidgetItem("Дата")
        self.result_value = QTableWidgetItem(result_value)
        self.mark_value = QTableWidgetItem("Оценка \nрезультата")
        self.comment_value = QTableWidgetItem("Комментарий к результату")

        self.table.setHorizontalHeaderItem(0, self.date_value)
        self.table.setHorizontalHeaderItem(1, self.result_value)
        self.table.setHorizontalHeaderItem(2, self.mark_value)
        self.table.setHorizontalHeaderItem(3, self.comment_value)

        stylesheet1 = "::section{Background-color:#FFC973}"
        self.table.horizontalHeader().setStyleSheet(stylesheet1)
        stylesheet = "::section{Background-color:#E6E6FA}"
        self.table.verticalHeader().setStyleSheet(stylesheet)

        self.fill_table()

        self.title_delete_entry = QLabel("<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">"
                                         "Удалить запись:</span></p></body></html>", self)
        self.title_delete_entry.setGeometry(450, 480, 141, 21)

        self.delete_row_of_entry = QLineEdit(self)
        self.delete_row_of_entry.setPlaceholderText("Введите номер строки, которую хотите удалить")
        self.delete_row_of_entry.setGeometry(450, 520, 291, 22)

        self.btn_delete_entry = QPushButton("Удалить запись", self)
        self.btn_delete_entry.setGeometry(450, 560, 187, 28)
        self.btn_delete_entry.clicked.connect(self.delete_entry)

        self.btn_delete_task = QPushButton("Удалить задачу", self)
        self.btn_delete_task.setGeometry(450, 410, 291, 28)
        self.btn_delete_task.clicked.connect(self.delete_task)

        self.exit_to_authorization = QPushButton("Выход", self)
        self.exit_to_authorization.setGeometry(450, 620, 291, 48)
        self.exit_to_authorization.clicked.connect(self.back_window_authorization)
        self.exit_to_authorization.setStyleSheet(light_blue_color)

    def download_chart(self, is_show=False):
        task = self.btn_open_task.currentText()
        task_names = db.get_task_names(self.id_person)
        index_task = task_names.index(task)
        measurements = db.get_measurements(self.id_person)
        measurement = measurements[index_task]
        results = db.get_results(self.id_person)[index_task]
        dates = db.get_dates(self.id_person)[index_task]
        if measurement == "Число":
            label_result = "Результат"
        elif measurement == "Время":
            results = list(map(lambda x: x.hour * 3600 + x.minute * 60 + x.second, results))
            label_result = "Результат (с)"
        else:
            label_result = f"Результат ({measurement})"
        number_of_records_for_plotting = get_number_of_records_for_plotting(self)
        values = pd.Series(results, index=dates)
        if number_of_records_for_plotting != "all_records":
            values = pd.Series(results, index=dates)[:number_of_records_for_plotting + 1]
        chart = Chart(self, values, label_result)
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
                self.date_value.text(),
                self.result_value.text(),
                self.mark_value.text(),
                self.comment_value.text()
            ])
            for i in range(self.table.rowCount()):
                writer.writerow([
                    self.table.item(i, 0).text(),
                    self.table.item(i, 1).text(),
                    self.table.item(i, 2).text(),
                    self.table.item(i, 3).text()
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

    def create_new_task(self, is_login_account=False, ex_main_window=None, parent=None, username=None, password=None):
        self.new_task = CreateTask(
            self.btn_open_task,
            self.result_value,
            self.table,
            self.id_person,
            is_login_account,
            ex_main_window,
            parent,
            username,
            password
        )
        self.new_task.show()

    def add_entry_to_table(self):
        self.add_entry = AddEntry(
            self.btn_open_task,
            self.table,
            self.id_person
        )
        self.add_entry.show()

    def fill_table(self, task=None):
        """ Метод заполняющий таблицу данными """
        if task is None:
            task = self.btn_open_task.currentText()
        if task:  # Если текст задания не пустой
            task_names = db.get_task_names(self.id_person)
            index_task = task_names.index(task)
            results = db.get_results(self.id_person)[index_task]
            dates = db.get_dates(self.id_person)[index_task]
            marks = db.get_marks(self.id_person)[index_task]
            comments = db.get_comments(self.id_person)[index_task]
            row = 0
            self.table.setRowCount(len(results))
            for result, date, mark, comment in zip(results, dates, marks, comments):
                time = str(date.time())[:-3]  # Преобразуем в формат hh:mm
                date = ".".join(str(date.date()).split("-")[::-1])  # Преобразуем в формат dd.mm.yy
                self.table.setItem(row, 0, QTableWidgetItem(f"{date} {time}"))
                self.table.setItem(row, 1, QTableWidgetItem(str(result)))
                self.table.setItem(row, 2, QTableWidgetItem(mark))
                self.table.setItem(row, 3, QTableWidgetItem(comment))
                row += 1

    def open_task(self, index, is_deleting_task=False, task=None):
        """ Метод, открывающий выбранное пользователем задание и заполняющий таблицу """
        if not is_deleting_task:
            task = self.btn_open_task.model().itemFromIndex(index).text()
        task_names = db.get_task_names(self.id_person)
        index_task = task_names.index(task)
        result_name = db.get_result_names(self.id_person)[index_task]
        measurements = db.get_measurements(self.id_person)
        measurement = measurements[index_task]
        if measurement not in ["Число", "Время"]:
            result_name = f"{result_name} ({measurement})"
        self.result_value.setText(result_name)
        self.table.setHorizontalHeaderItem(1, self.result_value)
        self.fill_table(task)
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

    def delete_entry(self):
        number_entry = self.delete_row_of_entry.text()
        try:
            number_entry = int(number_entry) - 1
        except ValueError:
            warning_dialog_window.is_not_number()
            return
        task = self.btn_open_task.currentText()
        task_names = db.get_task_names(self.id_person)
        index_task = task_names.index(task)
        results = db.get_results(self.id_person)
        dates = db.get_dates(self.id_person)
        marks = db.get_marks(self.id_person)
        comments = db.get_comments(self.id_person)
        if (len(results[index_task]) < number_entry + 1) or number_entry < 0:
            warning_dialog_window.row_not_exists()
        else:
            # Удаляем элементы с номером строки, который ввели
            del results[index_task][number_entry]
            del dates[index_task][number_entry]
            del marks[index_task][number_entry]
            del comments[index_task][number_entry]
            self.delete_row_of_entry.clear()
            # Заполняем таблицу с новыми данными
            row = 0
            self.table.setRowCount(len(results[index_task]))
            for result, date, mark, comment in zip(results[index_task], dates[index_task], marks[index_task],
                                                   comments[index_task]):
                time = str(date.time())[:-3]  # Преобразуем в формат hh:mm
                date = ".".join(str(date.date()).split("-")[::-1])  # Преобразуем в формат dd.mm.yy
                self.table.setItem(row, 0, QTableWidgetItem(f"{date} {time}"))
                self.table.setItem(row, 1, QTableWidgetItem(str(result)))
                self.table.setItem(row, 2, QTableWidgetItem(mark))
                self.table.setItem(row, 3, QTableWidgetItem(comment))
                row += 1
            # Добавляем в бд новые данные после удаления
            db.set_results(self.id_person, results)
            db.set_dates(self.id_person, dates)
            db.set_marks(self.id_person, marks)
            db.set_comments(self.id_person, comments)

    def delete_task(self):
        task = self.btn_open_task.currentText()
        task_names = db.get_task_names(self.id_person)
        if len(task_names) > 1:
            answer = warning_dialog_window.want_delete_task(self)
            if answer:
                index_task = task_names.index(task)
                result_names = db.get_result_names(self.id_person)
                measurements = db.get_measurements(self.id_person)
                results = db.get_results(self.id_person)
                dates = db.get_dates(self.id_person)
                marks = db.get_marks(self.id_person)
                comments = db.get_comments(self.id_person)
                # Удаляем, все, что связано с этим заданием
                self.btn_open_task.removeItem(index_task)
                del task_names[index_task]
                del result_names[index_task]
                del measurements[index_task]
                del results[index_task]
                del dates[index_task]
                del marks[index_task]
                del comments[index_task]
                # Добавляем в бд новые данные после удаления
                db.set_result_names(self.id_person, result_names)
                db.set_task_names(self.id_person, task_names)
                db.set_measurements(self.id_person, measurements)
                db.set_results(self.id_person, results)
                db.set_dates(self.id_person, dates)
                db.set_marks(self.id_person, marks)
                db.set_comments(self.id_person, comments)
                # Открываем первое задание
                self.btn_open_task.setCurrentIndex(0)
                self.open_task(
                    0,
                    is_deleting_task=True,
                    task=task_names[0]
                )

        else:
            warning_dialog_window.last_task_cannot_be_deleted()

    def back_window_authorization(self):
        self.close()
        self.authorization = self.dad()
        self.authorization.show()
