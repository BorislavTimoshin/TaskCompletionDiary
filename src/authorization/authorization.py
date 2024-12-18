import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from src.authorization.login import Login
from src.authorization.registration import Registration


class Authorization(QMainWindow):
    def __init__(self, main_window, translations: dict, current_language: str):
        super().__init__()
        uic.loadUi(f"Design/{current_language}/authorization/authorization.ui", self)
        self.main_window = main_window
        self.translations = translations
        self.current_language = current_language
        self.initUI()

    def initUI(self) -> None:
        self.btn_login.clicked.connect(self.open_login_window)
        self.btn_registration.clicked.connect(self.open_registration_window)
        self.CB_languages.currentTextChanged.connect(self.change_language)
        self.btn_logout.clicked.connect(self.logout)

    def change_language(self, language: str) -> None:
        """Translation of authorization text from one language to another"""
        self.current_language = language
        uic.loadUi(f"Design/{language}/authorization/authorization.ui", self)
        self.initUI()

    def open_login_window(self) -> None:
        self.close()
        self.ex_login = Login(
            main_window=self.main_window,
            authorization=Authorization,
            translations=self.translations,
            current_language=self.current_language,
        )
        self.ex_login.show()

    def open_registration_window(self) -> None:
        self.close()
        self.ex_registration = Registration(
            main_window=self.main_window,
            authorization=Authorization,
            translations=self.translations,
            current_language=self.current_language,
        )
        self.ex_registration.show()

    @staticmethod
    def logout() -> None:
        """Exit from application"""
        sys.exit()
