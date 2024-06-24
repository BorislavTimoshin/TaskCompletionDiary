from PyQt5.QtWidgets import QLineEdit, QComboBox, QFormLayout
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QCloseEvent
from Py_files.warnings import warning_dialog_window
from Py_files.database import db


class CreateTask(QDialog):
    def __init__(self, ex_main_window=None):
        super().__init__()
        self.ex_main_window = ex_main_window
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle("Создание задачи")

        task_creation_btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        creatingTaskFormLayout = QFormLayout(self)

        self.title_task_name = "Название задачи (не более 20 символов)"
        self.LE_task_name = QLineEdit(self)
        self.LE_task_name.setPlaceholderText("Например, бег по утрам")
        creatingTaskFormLayout.addRow(self.title_task_name, self.LE_task_name)

        self.title_result_name = "Название результата (не более 15 символов)"
        self.LE_result_name = QLineEdit(self)
        self.LE_result_name.setPlaceholderText("Например, расстояние")
        creatingTaskFormLayout.addRow(self.title_result_name, self.LE_result_name)

        self.title_unit_of_measure = "Единица измерения результата"
        self.CB_measure = QComboBox(self)
        measures = ["Число", "кг", "см", "м", "км", "м/с", "км/ч", "Время"]
        self.CB_measure.addItems(measures)
        creatingTaskFormLayout.addRow(self.title_unit_of_measure, self.CB_measure)

        creatingTaskFormLayout.addWidget(task_creation_btns)
        task_creation_btns.accepted.connect(self.ok)
        task_creation_btns.rejected.connect(self.cancel)

    def ok(self) -> None:
        """ Processing data to create a task """
        task_name = self.LE_task_name.text()
        result_name = self.LE_result_name.text()
        measure = self.CB_measure.currentText()
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
                task_names = db.get_task_names(self.ex_main_window.user_id)
                if task_name in task_names:  # Checking the existence of a task with the same name
                    warning_dialog_window.task_already_exists()
                else:
                    db.add_task(task_name, result_name, measure, self.ex_main_window.user_id)
                    # Adding a unit of measurement to the result name (if possible)
                    if measure not in ["Число", "Время"]:
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
