from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from src.database import db


class Login(QMainWindow):
    def __init__(self, main_window, authorization, translations: dict, current_language: str):
        super().__init__()
        uic.loadUi(f"Design/{current_language}/authorization/authorization.ui", self)
        self.main_window = main_window
        self.authorization = authorization
        self.translations = translations
        self.current_language = current_language
        self.initUI()

    def initUI(self) -> None:
        self.btn_login.clicked.connect(self.login_to_account)
        self.btn_back.clicked.connect(self.back)
        self.CB_languages.currentTextChanged.connect(self.change_language)
        self.lbl_wrong_name_or_password.hide()

    def change_language(self, language: str) -> None:
        """Translation of authorization text from one language to another"""
        self.current_language = language
        uic.loadUi(f"Design/{language}/authorization/authorization.ui", self)
        self.initUI()

    def login_to_account(self) -> None:
        login = self.LE_login.text()
        password = self.LE_password.text()
        if login and password:
            if db.user_exists(login, password):
                user_id = db.get_user_id(login)
                self.open_main_window(user_id)
            else:
                self.lbl_wrong_name_or_password.show()

    def back(self) -> None:
        """Return from authorization to authorization"""
        self.close()
        self.ex_authorization = self.authorization(
            main_window=self.main_window,
            translations=self.translations,
            current_language=self.current_language,
        )
        self.ex_authorization.show()

    def open_main_window(self, user_id: int) -> None:
        self.close()
        self.ex_main_window = self.main_window(
            user_id=user_id,
            current_language=self.current_language,
        )
        self.ex_main_window.show()
