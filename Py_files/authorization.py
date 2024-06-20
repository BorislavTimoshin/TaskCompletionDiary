from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from Py_files.login import Login
from Py_files.registration import Registration
from Py_files.colors import *
import sys


class Authorization(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(600, 200, 700, 500)
        self.setWindowTitle("Авторизация")

        # Authorization icon

        self.pixmap_authorization = QPixmap("Images/authorization.gif")
        self.lbl_image_authorization = QLabel(self)
        self.lbl_image_authorization.setGeometry(30, 70, 320, 320)
        self.lbl_image_authorization.setPixmap(self.pixmap_authorization)

        # Authorization text

        self.lbl_main = QLabel(
            "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">"
            "Дневник выполнения спортивных задач</span></p></body></html>",
            self
        )
        self.lbl_main.setGeometry(70, 40, 581, 41)

        self.lbl_authorization = QLabel(
            "<html><head/><body><p><span style=\" font-size:13pt; font-weight:600;\">"
            "Авторизация аккаунта</span></p></body></html>",
            self
        )
        self.lbl_authorization.setGeometry(330, 110, 261, 61)

        self.lbl_about_authorization = QLabel(
            "<html><head/><body><p><span style=\" font-size:10pt;\">"
            "Хотите войти или зарегистрироваться?</span></p></body></html>",
            self
        )
        self.lbl_about_authorization.setGeometry(330, 170, 351, 21)

        # Login

        self.btn_login = QPushButton("Войти", self)
        self.btn_login.setGeometry(330, 210, 181, 28)
        self.btn_login.setStyleSheet(light_blue_color)
        self.btn_login.clicked.connect(self.open_login_window)

        # Registration

        self.btn_registration = QPushButton("Регистрация", self)
        self.btn_registration.setGeometry(330, 260, 181, 28)
        self.btn_registration.setStyleSheet(light_blue_color)
        self.btn_registration.clicked.connect(self.open_registration_window)

        # Exit from application

        self.btn_logout = QPushButton("Закрыть", self)
        self.btn_logout.setGeometry(50, 415, 161, 31)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_logout.setStyleSheet(light_blue_color)

    def open_login_window(self) -> None:
        self.close()
        self.login = Login(
            main_window=self.main_window,
            authorization=Authorization
        )
        self.login.show()

    def open_registration_window(self) -> None:
        self.close()
        self.registration = Registration(
            main_window=self.main_window,
            authorization=Authorization
        )
        self.registration.show()

    @staticmethod
    def logout() -> None:
        """ Exit from application """
        sys.exit()
