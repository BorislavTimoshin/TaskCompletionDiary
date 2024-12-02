import pandas as pd
from PyQt5 import uic
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from src.database import db
from src.notifications import notifications


class UserDataForChart(QDialog):
    user_data_received = pyqtSignal(pd.Series)

    def __init__(self, ex_main_window, translations: dict):
        super().__init__()
        uic.loadUi(f"Design/{ex_main_window.current_language}/user_data_for_chart.ui", self)
        self.ex_main_window = ex_main_window
        self.translations = translations
        self.current_language = ex_main_window.current_language
        self.user_id = ex_main_window.user_id
        self.initUI()

    def initUI(self) -> None:
        # Processing Ok and Cancel buttons

        self.dialog_btns.accepted.connect(self.accept)
        self.dialog_btns.rejected.connect(self.cancel)

        ok_button_text = self.translations[self.current_language]["btn"]["ok"]
        cancel_button_text = self.translations[self.current_language]["btn"]["cancel"]

        self.dialog_btns.button(QDialogButtonBox.Ok).setText(ok_button_text)
        self.dialog_btns.button(QDialogButtonBox.Cancel).setText(cancel_button_text)

    def accept(self) -> None:
        """Processing data to plotting and getting an exemplar of the
        Chart class, thanks to which you can work with the chart:
        demonstrate, download, and more"""
        current_task = self.ex_main_window.CB_tasks.currentText()
        if self.were_errors(current_task):
            return
        first_result = self.LE_first_result.text()
        last_result = self.LE_last_result.text()
        if self.ex_main_window.is_table_row_number(first_result):
            if self.ex_main_window.is_table_row_number(last_result):
                first_result, last_result = sorted(map(int, (first_result, last_result)))
                # Getting task results and dates on which they were completed
                results = db.get_results(current_task, self.user_id)
                dates = db.get_dates(current_task, self.user_id)
                points = pd.Series(results, index=dates)[first_result - 1:last_result]
                self.user_data_received.emit(points)
                self.reject()

    def were_errors(self, task_name: str) -> bool:
        """Handling the very first errors, without which further program execution is pointless"""
        # If there are no tasks, then an error
        if not task_name:
            notifications.cause_error("taskNotCreated", self.current_language)
            return True
        # If there are no achievements, then there is an error
        number_of_achievements = db.get_number_of_achievements(task_name, self.user_id)
        if number_of_achievements == 0:
            notifications.cause_error("noAchievementsToPlot", self.current_language)
            return True
        return False

    def cancel(self) -> None:
        """Closing the dialog box (UserDataForChart) by clicking on "cancel" """
        self.reject()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Closing the dialog box (UserDataForChart) by clicking on the red cross"""
        event.accept()
