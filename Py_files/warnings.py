from PyQt5.QtWidgets import QMessageBox


# Было бы прикольно добавить срез данных, допустим, за предыдущие 7 дней по всем задачам (посмотреть текущую форму спортсмена)
# Было бы прикольно добавить возможность просмотреть комментарий пошире, а то места мало
# Было бы прикольно добавить возможность изменять дату, результат, оценку, комментарий прямо из таблицы
# Сделать иконку для .exe файла
# Сделать возможность поменять язык
# Заменить на Скачать -> График, Таблица
# Надо подумать, как модифицировать график, когда данных много, так как множество жирных точек выглядит некрасиво
# TODO добавить обработку реультата с единицей измерения ВРЕМЯ

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
    def is_not_integer():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Введенное значение не является целым числом")
        msg.setWindowTitle("Ошибка в указании целого числа")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def line_number_not_exist():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Номера данной строки не существует              ")
        msg.setWindowTitle("Ошибка в написании номера удаления строки")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def no_achievements_to_plot():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Нет достижений для построения графика")
        msg.setWindowTitle("Ошибка в построении графика")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def task_not_created():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Задача не создана              ")
        msg.setWindowTitle("Ошибка в создании задачи")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def delete_task_or_not(parent) -> bool:
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

    @staticmethod
    def replace_with_similar_date(parent) -> bool:
        msg = QMessageBox()
        answer = msg.question(
            parent,
            "Ошибка в указании даты",
            "Результат с такой датой уже есть в таблице. Хотите заменить?",
            msg.Yes | msg.No
        )
        if answer == msg.Yes:
            return True
        if answer == msg.No:
            return False


warning_dialog_window = WarningDialogWindow()
