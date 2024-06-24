from PyQt5.QtWidgets import QLineEdit, QTimeEdit, QComboBox
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QVBoxLayout
from PyQt5.QtGui import QCloseEvent
from Py_files.warnings import warning_dialog_window
from Py_files.database import db
import datetime


class AddAchievementToTable(QDialog):
    def __init__(self, ex_main_window=None):
        super().__init__()
        self.ex_main_window = ex_main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Добавление записи")
        self.setGeometry(550, 200, 800, 700)

        add_achievement_btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        add_achievement_btns.move(580, 600)

        task_name = self.ex_main_window.CB_tasks.currentText()
        result_name, measure = db.get_task(task_name, self.ex_main_window.user_id)

        self.lbl_indicate_result = QLabel(
            f"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
            f"Укажите {result_name}:</span></p></body></html>",
            self
        )
        self.lbl_indicate_result.setGeometry(10, 0, 331, 31)

        self.LE_result_in_form_int = QLineEdit(self)
        self.LE_result_in_form_int.setGeometry(10, 40, 261, 31)
        self.LE_result_in_form_int.hide()

        self.TE_result_in_form_time = QTimeEdit(self)
        self.TE_result_in_form_time.setDisplayFormat("hh:mm:ss")
        self.TE_result_in_form_time.setGeometry(10, 40, 261, 31)
        self.TE_result_in_form_time.hide()

        if measure == "Время":
            self.TE_result_in_form_time.show()
        else:
            self.LE_result_in_form_int.show()

        self.lbl_indicate_mark = QLabel(
            "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
            "Укажите оценку результата</span></p></body></html>",
            self
        )
        self.lbl_indicate_mark.setGeometry(10, 90, 271, 31)

        self.CB_mark = QComboBox(self)
        self.CB_mark.addItems(["1", "2", "3", "4", "5"])
        self.CB_mark.setGeometry(10, 130, 261, 31)

        self.lbl_write_comment = QLabel(
            "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
            "Напишите комментарий к результату (По желанию)</span></p></body></html>",
            self
        )
        self.lbl_write_comment.setGeometry(10, 180, 641, 31)

        self.LE_comment = QLineEdit(self)
        self.LE_comment.setGeometry(10, 220, 451, 40)

        self.lbl_indicate_data = QLabel(
            "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
            "Укажите дату выполнения спортивной задачи:</span></p></body></html>",
            self
        )
        self.lbl_indicate_data.setGeometry(10, 295, 420, 30)

        self.addingAchievementWidget = QWidget(self)
        self.addingAchievementWidget.setContentsMargins(0, 0, 0, 0)
        self.addingAchievementWidget.setGeometry(15, 335, 400, 300)

        self.addingAchievementVLayout = QVBoxLayout(self.addingAchievementWidget)
        self.addingAchievementVLayout.setContentsMargins(0, 0, 0, 0)

        self.calendarWidget = QCalendarWidget(self.addingAchievementWidget)
        self.addingAchievementVLayout.addWidget(self.calendarWidget)

        add_achievement_btns.accepted.connect(self.accept)
        add_achievement_btns.rejected.connect(self.cancel)

    def get_date_of_achievement(self) -> datetime.date:
        """ Getting the date on which the achievement was completed """
        date = datetime.date(
            year=self.calendarWidget.selectedDate().year(),
            month=self.calendarWidget.selectedDate().month(),
            day=self.calendarWidget.selectedDate().day()
        )
        return date

    def accept(self) -> None:
        """ Processing data to add achievement to the table """
        task_name = self.ex_main_window.CB_tasks.currentText()
        current_date = self.get_date_of_achievement()
        previous_dates = db.get_dates(task_name, self.ex_main_window.user_id)
        mark = self.CB_mark.currentText()
        comment = self.LE_comment.text()
        measure = db.get_measure(task_name, self.ex_main_window.user_id)
        # Checking the correctness of the entered result
        if measure == "Время":
            result = self.TE_result_in_form_time.time()
            result = result.hour() * 3600 + result.minute() * 60 + result.second()
        else:
            try:
                result = float(self.LE_result_in_form_int.text().replace(",", ".", 1))
                if result.is_integer():
                    result = int(result)
            except ValueError:
                warning_dialog_window.is_not_number()
                return
        # Checking whether an achievement occurred on a specified date
        if current_date in previous_dates:  # If a result with a similar date is already in the table
            if warning_dialog_window.replace_with_similar_date(self):  # We suggest replacing (first delete, then add)
                db.delete_achievement(current_date, task_name, self.ex_main_window.user_id)
            else:
                return
        # Closing a window
        self.reject()
        # Adding an achievement
        db.add_achievement(current_date, result, mark, comment, task_name, self.ex_main_window.user_id)
        self.ex_main_window.fill_table()
        self.ex_main_window.show()

    def cancel(self) -> None:
        """ Closing the dialog box (AddAchievementToTable) by clicking on "cancel" """
        self.reject()
        self.ex_main_window.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        """ Closing the dialog box (AddAchievementToTable) by clicking on the red cross """
        event.accept()
        self.ex_main_window.show()
