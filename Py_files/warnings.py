from PyQt5.QtWidgets import QMessageBox


# TODO Не обработана ошибка, если данных в таблице нет и человек хочет построить график, то программа падает
# Было бы прикольно добавить срез данных, допустим, за предыдущие 7 дней по всем задачам (посмотреть текущую форму спортсмена)
# Было бы прикольно добавить возможность просмотреть комментарий пошире, а то места мало
# Было бы прикольно добавить возможность изменять дату, результат, оценку, комментарий прямо из таблицы
# Сделать иконку для .exe файла
# Сделать возможность поменять язык
# Заменить на Скачать -> График, Таблица
# TODO Пользователь не найден. Если пароль неверный, но юзер есть, то заменить на пароль неверный
# TODO Добавить обработку события, когда нет никакой задачи, но при этом юзер хочет добавить запись или удалить задачу
# Надо подумать, как модифицировать график, когда данных много, так как множество жирных точек выглядит некрасиво
# Было б не плохо, чтобы после удадения записи, номер строки в LineEdit удалился
# Дописать описание работы с приложением


class WarningDialogWindow:
    @staticmethod
    def len_task_name_is_0():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Название задачи не может быть пустым")
        msg.setWindowTitle("Ошибка в названии задачи")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def len_task_name_more_30():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Длина названия задачи должна быть не более 30 символов")
        msg.setWindowTitle("Ошибка в названии задачи")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def len_result_name_is_0():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Название результата не может быть пустым")
        msg.setWindowTitle("Ошибка в названии результата")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def len_result_name_more_15():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Длина названия результата должна быть не более 15 символов")
        msg.setWindowTitle("Ошибка в названии результата")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def task_already_exists():
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
    def line_number_not_exist():
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
    def delete_task_or_not(parent):
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
