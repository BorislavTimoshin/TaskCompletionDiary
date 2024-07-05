import json

from PyQt5.QtWidgets import QMessageBox


with open("data/translations.json", "r", encoding="utf-8") as file:
    translations = json.load(file)


class Notification:
    @staticmethod
    def cause_error(error_name: str, language: str) -> None:
        """Throwing an error, an exception asking you to change something"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        # Processing error text

        error_text = translations[language]["errors"][error_name]
        window_title = translations[language]["windowTitle"]["errors"][error_name]
        msg.setText(error_text)
        msg.setWindowTitle(window_title)

        # Processing Ok and Cancel buttons

        ok_button_text = translations[language]["btn"]["ok"]
        cancel_button_text = translations[language]["btn"]["cancel"]
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.button(QMessageBox.Ok).setText(ok_button_text)
        msg.button(QMessageBox.Cancel).setText(cancel_button_text)

        msg.exec()

    @staticmethod
    def ask_question(parent, question_name: str, language: str) -> bool:
        """Asks a question to find out if something is worth changing or doing"""
        msg = QMessageBox()

        # Processing question text

        window_title = translations[language]["windowTitle"]["questions"][question_name]
        question_text = translations[language]["questions"][question_name]
        answer = msg.question(
            parent,
            window_title,
            question_text,
            msg.Yes | msg.No,
        )

        if answer == msg.Yes:
            return True
        return False


notifications = Notification()
