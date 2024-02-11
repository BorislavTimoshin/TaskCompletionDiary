from PyQt5.QtWidgets import QMessageBox


# Класс для вывода диалоговых окон с предупреждениями
class WarningDialogWindow:
    @staticmethod
    def len_task_more_20():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Длина названия задачи должна быть не более 20 символов")
        msg.setWindowTitle("Ошибка в названии задачи")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def len_title_result_more_15():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Длина названия результата должна быть не более 15 символов")
        msg.setWindowTitle("Ошибка в названии результата")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def task_exists():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Задание с таким именем уже существует")
        msg.setWindowTitle("Ошибка в названии задачи")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def is_not_number():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Введенное значение не является числом")
        msg.setWindowTitle("Ошибка в указании числа")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def len_comment_more_45():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Длина комментария не может быть больше 45 символов")
        msg.setWindowTitle("Ошибка в написании комментария")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def row_not_exists():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Номера данной строки не существует")
        msg.setWindowTitle("Ошибка в написании номера удаления строки")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def last_task_cannot_be_deleted():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Последняя задача не может быть удалена")
        msg.setWindowTitle("Ошибка в удалении задачи")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def want_delete_task(parent):
        msg = QMessageBox()
        answer = msg.question(
            parent,
            "Удаление задачи",
            "Хотите удалить задачу? Восстановление будет невозможно",
            msg.Yes | msg.No
        )
        if answer == msg.Yes:
            return True
        if answer == msg.No:
            return False


warning_dialog_window = WarningDialogWindow()
