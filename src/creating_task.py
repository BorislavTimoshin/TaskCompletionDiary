from PyQt5 import uic
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from src.database import db
from src.notifications import notifications


class CreateTask(QDialog):
    def __init__(self, ex_main_window, translations: dict):
        super().__init__()
        uic.loadUi(f"Design/{ex_main_window.current_language}/creating_task.ui", self)
        self.ex_main_window = ex_main_window
        self.translations = translations
        self.current_language = ex_main_window.current_language
        self.user_id = self.ex_main_window.user_id
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
        """Processing data to create a task"""
        task_name = self.LE_task_name.text()
        result_name = self.LE_result_name.text()
        units = (
            "number",
            "kilogram",
            "centimeter",
            "meter",
            "kilometer",
            "meterPerSecond",
            "kilometerPerHour",
            "time",
        )
        unit = units[self.CB_units.currentIndex()]
        # Checking for empty task name and result name
        if not task_name:
            notifications.cause_error("taskNameCannotBeEmpty", self.current_language)
            return
        if not result_name:
            notifications.cause_error("resultNameCannotBeEmpty", self.current_language)
            return
        # Checking the task name and result name for valid length
        if len(task_name) <= 30:
            if len(result_name) <= 15:
                task_names = db.get_task_names(self.user_id)
                if task_name in task_names:  # Checking the existence of a task with the same name
                    notifications.cause_error("taskAlreadyExists", self.current_language)
                else:
                    db.add_task(task_name, result_name, unit, self.user_id)
                    # Adding a unit of measurement to the result name (if possible)
                    if unit not in ("number", "time"):
                        unit_abbr = self.translations[self.current_language]["unit"][unit]
                        result_name = f"{result_name} ({unit_abbr})"
                    # Adding task data to the application
                    self.ex_main_window.CB_tasks.addItem(task_name)
                    self.ex_main_window.CB_tasks.setCurrentText(task_name)
                    self.ex_main_window.resultTableWidget.setText(result_name)
                    # Closing the dialog box (CreateTask)
                    self.reject()
            else:
                notifications.cause_error("lenResultNameMore15", self.current_language)
        else:
            notifications.cause_error("lenTaskNameMore30", self.current_language)

    def cancel(self) -> None:
        """Closing the dialog box (CreateTask) by clicking on "cancel" """
        self.reject()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Closing the dialog box (CreateTask) by clicking on the red cross"""
        event.accept()
