from PyQt5.QtWidgets import QMessageBox
import json

with open("Other_files/translations.json", "r", encoding="utf-8") as file:
    translations = json.load(file)


class WarningDialogWindow:
    @staticmethod
    def cause_error(error_name: str, language: str) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        # Processing error text

        error_text = translations[language]["warnings"][error_name]
        window_title = translations[language]["windowTitle"]["warnings"][error_name]
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
        msg = QMessageBox()

        # Processing question text

        window_title = translations[language]["windowTitle"]["questions"][question_name]
        question_text = translations[language]["questions"][question_name]
        answer = msg.question(
            parent,
            window_title,
            question_text,
            msg.Yes | msg.No
        )

        # Processing Yes and No buttons

        yes_button_text = translations[language]["btn"]["yes"]
        no_button_text = translations[language]["btn"]["no"]

        msg.button(QMessageBox.Yes).setText(yes_button_text)
        msg.button(QMessageBox.No).setText(no_button_text)

        if answer == msg.Yes:
            return True
        if answer == msg.No:
            return False


warnings = WarningDialogWindow()
