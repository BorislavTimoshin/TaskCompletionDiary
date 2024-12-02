from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QDialogButtonBox


class Help(QDialog):
    def __init__(self, translations: dict, current_language: str):
        super().__init__()
        self.translations = translations
        self.current_language = current_language

    def initUI(self) -> None:
        # Processing the "OK" button

        self.dialog_btns.accepted.connect(self.accept)
        ok_button_text = self.translations[self.current_language]["btn"]["ok"]
        self.dialog_btns.button(QDialogButtonBox.Ok).setText(ok_button_text)

    def show_about(self) -> None:
        """Viewing the dialog box: description of the program,
        rules for working with the application"""
        uic.loadUi(f"Design/{self.current_language}/about.ui", self)
        self.initUI()
        self.show()

    def show_version(self) -> None:
        """View dialog box: program version; created for developers"""
        uic.loadUi(f"Design/{self.current_language}/version.ui", self)
        self.initUI()
        self.show()
