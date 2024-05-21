from PyQt5.QtWidgets import QLineEdit, QTimeEdit, QComboBox
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QPlainTextEdit
from PyQt5.QtGui import QPixmap
from datetime import datetime, time
from Py_files.warnings import warning_dialog_window
from Py_files.database import db


# Класс для открытия окна: открыть задание
class CreateTask(QDialog):
    def __init__(self, btn_open_task, result_value, table, id_person=None, is_login_account=False, ex_main_window=None,
                 parent=None, username=None, password=None):
        super().__init__(parent)
        self.btn_open_task = btn_open_task
        self.result_value = result_value
        self.table = table
        self.id_person = id_person
        self.is_login_account = is_login_account
        self.ex_main_window = ex_main_window
        self.parent = parent
        self.username = username
        self.password = password
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Новая задача")

        buttons_new_task = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        form_layout = QFormLayout(self)

        self.title_name_task = "Название задачи (не более 20 символов)"
        self.name_task = QLineEdit(self)
        self.name_task.setPlaceholderText("Например, бег по утрам")
        form_layout.addRow(self.title_name_task, self.name_task)

        self.title_name_result = "Название результата (не более 15 символов)"
        self.name_result = QLineEdit(self)
        self.name_result.setPlaceholderText("Например, расстояние")
        form_layout.addRow(self.title_name_result, self.name_result)

        self.title_unit_of_measurement = "Единица измерения результата"
        self.unit_of_measurement = QComboBox(self)
        self.unit_of_measurement.addItems(["Число", "кг", "см", "м", "км", "м/с", "км/ч", "Время"])
        form_layout.addRow(self.title_unit_of_measurement, self.unit_of_measurement)

        form_layout.addWidget(buttons_new_task)
        buttons_new_task.accepted.connect(self.ok)
        buttons_new_task.rejected.connect(self.cancel)

    def ok(self):
        """ Метод для обработки создания задания """
        task_name = self.name_task.text()
        result_name = self.name_result.text()
        measurement = self.unit_of_measurement.currentText()
        if task_name and result_name:
            if len(task_name) <= 30:
                if len(result_name) <= 15:
                    task_names = db.get_task_names(self.id_person)
                    if task_name in task_names:
                        warning_dialog_window.task_exists()
                    else:
                        db.set_new_task(self.id_person, task_name, result_name, measurement)
                        if measurement not in ["Число", "Время"]:
                            result_name = f"{result_name} ({measurement})"
                        self.reject()
                        self.btn_open_task.addItem(task_name)
                        self.btn_open_task.setCurrentText(task_name)
                        self.result_value.setText(result_name)
                        results = db.get_results(self.id_person)
                        dates = db.get_dates(self.id_person)
                        marks = db.get_marks(self.id_person)
                        comments = db.get_comments(self.id_person)
                        db.set_results(self.id_person, results + [[]])
                        db.set_dates(self.id_person, dates + [[]])
                        db.set_marks(self.id_person, marks + [[]])
                        db.set_comments(self.id_person, comments + [[]])
                        self.table.setHorizontalHeaderItem(1, self.result_value)
                        self.table.setRowCount(0)
                        if self.is_login_account:
                            self.parent.close()
                            self.ex_main_window.show()
                else:
                    warning_dialog_window.len_title_result_more_15()
            else:
                warning_dialog_window.len_task_more_30()

    def cancel(self):
        self.reject()
        if self.is_login_account:
            db.delete_person(self.id_person)

    def closeEvent(self, event):
        event.accept()
        if self.is_login_account:
            db.delete_person(self.id_person)


# Класс для открытия окна: добавить запись в таблицу
class AddEntry(QDialog):
    def __init__(self, btn_open_task, table, id_person=None):
        super().__init__()
        self.btn_open_task = btn_open_task
        self.table = table
        self.id_person = id_person
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Добавить запись")
        self.setGeometry(550, 200, 800, 700)

        buttons_add_entry = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons_add_entry.move(580, 600)

        self.title_result = QLabel(f"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
                                   f"Укажите {self.get_result_name()}:</span></p></body></html>", self)
        self.title_result.setGeometry(10, 0, 331, 31)

        self.result_in_form_int = QLineEdit(self)
        self.result_in_form_int.setGeometry(10, 40, 261, 31)
        self.result_in_form_int.hide()

        self.result_in_form_time = QTimeEdit(self)
        self.result_in_form_time.setDisplayFormat("hh:mm:ss")
        self.result_in_form_time.setGeometry(10, 40, 261, 31)
        self.result_in_form_time.hide()

        if self.get_measurement() == "Время":
            self.result_in_form_time.show()
        else:
            self.result_in_form_int.show()

        self.title_mark = QLabel("<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
                                 "Укажите оценку результата</span></p></body></html>", self)
        self.title_mark.setGeometry(10, 90, 271, 31)

        self.mark = QComboBox(self)
        self.mark.addItems(["1", "2", "3", "4", "5"])
        self.mark.setGeometry(10, 130, 261, 31)

        self.title_comment = QLabel("<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
                                    "Напишите комментарий к результату (По желанию)</span></p></body></html>", self)
        self.title_comment.setGeometry(10, 180, 641, 31)

        self.comment = QLineEdit(self)
        self.comment.setGeometry(10, 220, 451, 40)

        self.title_data = QLabel("<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
                                 "Укажите дату выполнения спортивной задачи:</span></p></body></html>", self)
        self.title_data.setGeometry(10, 295, 420, 30)

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget.setGeometry(15, 335, 400, 300)

        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.timeEdit = QTimeEdit(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.timeEdit)

        self.calendarWidget = QCalendarWidget(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.calendarWidget)

        buttons_add_entry.accepted.connect(self.accept)
        buttons_add_entry.rejected.connect(self.reject)

    def get_index_task(self):
        """ Получить индекс текущего выбранного задания в btn_open_task в списке заданий бд """
        task = self.btn_open_task.currentText()
        tasks = db.get_task_names(self.id_person)
        return tasks.index(task)

    def get_result_name(self):
        """ Получить имя результата, которое вставится в заголовок таблицы в соответствии с выбранным заданием """
        result_names = db.get_result_names(self.id_person)
        index_result = self.get_index_task()
        return result_names[index_result]

    def get_measurement(self):
        """ Получить единицу измерения результата """
        measurements = db.get_measurements(self.id_person)
        index_measurement = self.get_index_task()
        return measurements[index_measurement]

    def get_index_insertion(self, date, dates):
        """ Получить индекс в вставки в список списка: в список конкретного задания """
        index_task = self.get_index_task()
        dates = dates[index_task]
        start = 0
        end = len(dates)
        while start < end:
            mid = (start + end) // 2
            if dates[mid] > date:
                start = mid + 1
            else:
                end = mid
        return start

    def get_date(self):
        date = datetime(
            year=self.calendarWidget.selectedDate().year(),
            month=self.calendarWidget.selectedDate().month(),
            day=self.calendarWidget.selectedDate().day(),
            hour=self.timeEdit.time().hour(),
            minute=self.timeEdit.time().minute()
        )
        return date

    def insert_in_db(self, result, date, mark, comment):
        results = db.get_results(self.id_person)
        dates = db.get_dates(self.id_person)
        marks = db.get_marks(self.id_person)
        comments = db.get_comments(self.id_person)
        index_task = self.get_index_task()
        index_insert = self.get_index_insertion(date, dates)

        results[index_task].insert(index_insert, result)
        dates[index_task].insert(index_insert, date)
        marks[index_task].insert(index_insert, mark)
        comments[index_task].insert(index_insert, comment)
        self.table.setRowCount(len(results[index_task]))
        row = 0

        for result, date, mark, comment in zip(results[index_task], dates[index_task], marks[index_task],
                                               comments[index_task]):
            hh_mm = str(date.time())[:-3]  # Преобразуем в формат hh:mm
            date = ".".join(str(date.date()).split("-")[::-1])  # Преобразуем в формат dd.mm.yy
            self.table.setItem(row, 0, QTableWidgetItem(f"{date} {hh_mm}"))
            self.table.setItem(row, 1, QTableWidgetItem(str(result)))
            self.table.setItem(row, 2, QTableWidgetItem(mark))
            self.table.setItem(row, 3, QTableWidgetItem(comment))
            row += 1

        db.set_results(self.id_person, results)
        db.set_dates(self.id_person, dates)
        db.set_marks(self.id_person, marks)
        db.set_comments(self.id_person, comments)

    def accept(self):
        measurement = self.get_measurement()
        result = None
        if measurement == "Время":
            result = self.result_in_form_time.time()
            result = time(
                hour=result.hour(),
                minute=result.minute(),
                second=result.second()
            )
        else:
            try:
                result = float(self.result_in_form_int.text().replace(",", ".", 1))
                if result.is_integer():
                    result = int(result)
            except ValueError:
                warning_dialog_window.is_not_number()
        date = self.get_date()
        mark = self.mark.currentText()
        comment = self.comment.text()
        if result and mark and date:
            self.insert_in_db(result, date, mark, comment)
            self.close()


# Класс для открытия диалогового окна: о программе
class AboutProgram(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("О программе")
        self.setGeometry(650, 300, 610, 400)

        buttons_new_task = QDialogButtonBox(QDialogButtonBox.Ok, self)
        buttons_new_task.accepted.connect(self.accept)
        buttons_new_task.move(440, 360)

        self.pixmap_book = QPixmap("Images/book.png")
        self.book = QLabel(self)
        self.book.setGeometry(18, 85, 200, 218)
        self.book.setPixmap(self.pixmap_book)

        with open("Other_files/about_program.txt", "r", encoding="utf-8") as txt_file:
            text = txt_file.read()

        self.textEdit = QPlainTextEdit(text, self)
        self.textEdit.setGeometry(230, 40, 351, 301)
        self.textEdit.setReadOnly(True)


def get_number_of_records_for_plotting(parent):
    if parent.plotting_option_1.isChecked():
        return 30
    if parent.plotting_option_2.isChecked():
        return 60
    if parent.plotting_option_3.isChecked():
        return 90
    if parent.plotting_option_4.isChecked():
        return 120
    if parent.plotting_option_5.isChecked():
        return 150
    if parent.plotting_option_6.isChecked():
        return 180
    if parent.plotting_option_7.isChecked():
        return 270
    if parent.plotting_option_8.isChecked():
        return 365
    if parent.plotting_option_9.isChecked():
        return 730
    return "all_records"
