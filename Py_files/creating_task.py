from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic
from Py_files.warnings import warning_dialog_window
from Py_files.database import db


class CreateTask(QDialog):
    def __init__(self, ex_main_window, translations: dict, current_language: str):
        super().__init__()
        uic.loadUi(f"Design/{current_language}/creating_task.ui", self)
        self.ex_main_window = ex_main_window
        self.user_id = self.ex_main_window.user_id
        self.translations = translations
        self.current_language = current_language
        self.initUI()

    def initUI(self) -> None:
        # Processing Ok and Cancel buttons

        self.task_creation_dialog_btns.accepted.connect(self.accept)
        self.task_creation_dialog_btns.rejected.connect(self.cancel)

        ok_button_text = self.translations[self.current_language]["btn"]["ok"]
        cancel_button_text = self.translations[self.current_language]["btn"]["cancel"]

        self.task_creation_dialog_btns.button(QDialogButtonBox.Ok).setText(ok_button_text)
        self.task_creation_dialog_btns.button(QDialogButtonBox.Cancel).setText(cancel_button_text)

    def accept(self) -> None:
        """ Processing data to create a task """
        task_name = self.LE_task_name.text()
        result_name = self.LE_result_name.text()
        measure = self.CB_measures.currentText()
        # Checking for empty task name and result name
        if not task_name:
            warning_dialog_window.len_task_name_is_0()
            return
        if not result_name:
            warning_dialog_window.len_result_name_is_0()
            return
        # Checking the task name and result name for valid length
        if len(task_name) <= 30:
            if len(result_name) <= 15:
                task_names = db.get_task_names(self.user_id)
                if task_name in task_names:  # Checking the existence of a task with the same name
                    warning_dialog_window.task_already_exists()
                else:
                    db.add_task(task_name, result_name, measure, self.user_id)
                    # Adding a unit of measurement to the result name (if possible)
                    measure_is_number = self.translations[self.current_language]["measure"]["number"]
                    measure_is_time = self.translations[self.current_language]["measure"]["time"]
                    if measure not in [measure_is_number, measure_is_time]:
                        result_name = f"{result_name} ({measure})"
                    # Adding task data to the application
                    self.ex_main_window.CB_tasks.addItem(task_name)
                    self.ex_main_window.CB_tasks.setCurrentText(task_name)
                    self.ex_main_window.resultTableWidget.setText(result_name)
                    # Closing the dialog box (CreateTask)
                    self.reject()
            else:
                warning_dialog_window.len_title_result_more_15()
        else:
            warning_dialog_window.len_task_name_more_30()

    def cancel(self) -> None:
        """ Closing the dialog box (CreateTask) by clicking on "cancel" """
        self.reject()

    def closeEvent(self, event: QCloseEvent) -> None:
        """ Closing the dialog box (CreateTask) by clicking on the red cross """
        event.accept()
