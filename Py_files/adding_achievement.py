from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic
from Py_files.warnings import warnings
from Py_files.database import db
import datetime


class AddAchievementToTable(QDialog):
    def __init__(self, ex_main_window, translations: dict, current_language: str):
        super().__init__()
        uic.loadUi(f"Design/{current_language}/adding_entry.ui", self)
        self.ex_main_window = ex_main_window
        self.user_id = self.ex_main_window.user_id
        self.translations = translations
        self.current_language = current_language
        self.initUI()

    def initUI(self) -> None:
        # Line Edit processing for result

        self.LE_result_in_form_int.hide()
        self.TE_result_in_form_time.hide()

        task_name = self.ex_main_window.CB_tasks.currentText()
        measure = db.get_measure(task_name, self.user_id)
        measure_is_time = self.translations[self.current_language]["measure"]["time"]

        if measure == measure_is_time:  # If the task unit is time
            self.TE_result_in_form_time.show()
        else:
            self.LE_result_in_form_int.show()

        # Processing Ok and Cancel buttons

        self.adding_achievement_dialog_btns.accepted.connect(self.accept)
        self.adding_achievement_dialog_btns.rejected.connect(self.cancel)

        ok_button_text = self.translations[self.current_language]["btn"]["ok"]
        cancel_button_text = self.translations[self.current_language]["btn"]["cancel"]

        self.adding_achievement_dialog_btns.button(QDialogButtonBox.Ok).setText(ok_button_text)
        self.adding_achievement_dialog_btns.button(QDialogButtonBox.Cancel).setText(cancel_button_text)

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
        previous_dates = db.get_dates(task_name, self.user_id)
        mark = self.CB_marks.currentText()
        comment = self.LE_comment.text()
        measure = db.get_measure(task_name, self.user_id)
        measure_is_time = self.translations[self.current_language]["measure"]["time"]
        # Checking the correctness of the entered result
        if measure == measure_is_time:  # If the task unit is time
            result = self.TE_result_in_form_time.time()
            result = result.hour() * 3600 + result.minute() * 60 + result.second()
        else:
            try:
                result = float(self.LE_result_in_form_int.text().replace(",", ".", 1))
                if result.is_integer():
                    result = int(result)
            except ValueError:
                warnings.cause_error("isNotInteger", self.current_language)
                return
        # Checking whether an achievement occurred on a specified date
        if current_date in previous_dates:  # If a result with a similar date is already in the table
            replace_with_similar_date = warnings.ask_question(self, "replaceWithSimilarDate", self.current_language)
            if replace_with_similar_date:  # We suggest replacing (first delete, then add)
                db.delete_achievement(current_date, task_name, self.user_id)
            else:
                return
        # Closing a window
        self.reject()
        # Adding an achievement
        db.add_achievement(current_date, result, mark, comment, task_name, self.user_id)
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
