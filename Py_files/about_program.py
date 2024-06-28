from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5 import uic


class AboutProgram(QDialog):
    def __init__(self, translations: dict, current_language: str):
        super().__init__()
        self.translations = translations
        self.current_language = current_language

    def initUI(self) -> None:
        # Processing the "OK" button

        self.about_program_dialog_btns.accepted.connect(self.accept)
        ok_button_text = self.translations[self.current_language]["btn"]["ok"]
        self.about_program_dialog_btns.button(QDialogButtonBox.Ok).setText(ok_button_text)

    def show_program_description(self) -> None:
        """ Viewing the dialog box: description of the program, rules for working with the application """
        uic.loadUi(f"Design/{self.current_language}/program_description.ui", self)
        self.initUI()
        self.show()

    def show_program_version(self) -> None:
        """ View dialog box: program version; created for developers """
        uic.loadUi(f"Design/{self.current_language}/program_version.ui", self)
        self.initUI()
        self.show()
