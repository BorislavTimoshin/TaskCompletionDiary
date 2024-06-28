from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from Py_files.database import db


class Registration(QMainWindow):
    def __init__(self, main_window, authorization, translations: dict, current_language: str):
        super().__init__()
        uic.loadUi(f"Design/{current_language}/registration.ui", self)
        self.main_window = main_window
        self.authorization = authorization
        self.translations = translations
        self.current_language = current_language
        self.initUI()

    def initUI(self) -> None:
        self.btn_registration_and_login.clicked.connect(self.registration)
        self.btn_back.clicked.connect(self.back)
        self.CB_languages.currentTextChanged.connect(self.chage_language)
        self.lbl_login_already_exists.hide()

    def chage_language(self, language: str) -> None:
        """ Translation of registration text from one language to another """
        self.current_language = language
        uic.loadUi(f"Design/{language}/registration.ui", self)
        self.initUI()

    def registration(self) -> None:
        """ User registration: adding a user to the database """
        login = self.LE_login.text()
        password = self.LE_password.text()
        if login and password:
            if db.login_exists(login):
                self.lbl_login_already_exists.show()
            else:
                db.add_user(login, password)
                user_id = db.get_user_id(login)
                self.open_main_window(user_id)

    def back(self) -> None:
        """ Return from registration to authorization """
        self.close()
        self.ex_authorization = self.authorization(
            main_window=self.main_window,
            translations=self.translations,
            current_language=self.current_language
        )
        self.ex_authorization.show()

    def open_main_window(self, user_id: int) -> None:
        """ Creating a task and then opening the main window """
        self.close()
        self.ex_main_window = self.main_window(
            user_id=user_id,
            current_language=self.current_language
        )
        self.ex_main_window.show()
