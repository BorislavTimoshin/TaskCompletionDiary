import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from Py_files.login import Login
from Py_files.registration import Registration


# Класс для работы с окном: авторизация пользователя
class Authorization(QMainWindow):
    def __init__(self, dad=None):
        super().__init__()
        self.dad = dad
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 700, 500)
        self.setWindowTitle("Авторизация")

        self.pixmap_authorization = QPixmap("Images/authorization.gif")
        self.image_authorization = QLabel(self)
        self.image_authorization.move(30, 70)
        self.image_authorization.resize(320, 320)
        self.image_authorization.setPixmap(self.pixmap_authorization)

        self.main_title = QLabel("<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">"
                                 "Дневник выполнения спортивных задач</span></p></body></html>", self)
        self.main_title.setGeometry(70, 40, 581, 41)

        self.title_authorization = QLabel('<html><head/><body><p><span style=" font-size:13pt; font-weight:600;">'
                                          'Авторизация аккаунта</span></p></body></html>', self)
        self.title_authorization.setGeometry(330, 110, 261, 61)

        self.text_about_authorization = QLabel('<html><head/><body><p><span style=" font-size:10pt;">Хотите войти или '
                                               'зарегистрироваться?</span></p></body></html>', self)
        self.text_about_authorization.setGeometry(330, 170, 351, 21)

        self.btn_login = QPushButton("Войти", self)
        self.btn_login.setGeometry(330, 210, 181, 28)
        self.btn_login.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )
        self.btn_login.clicked.connect(self.open_login_window)

        self.btn_registration = QPushButton("Регистрация", self)
        self.btn_registration.setGeometry(330, 260, 181, 28)
        self.btn_registration.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )
        self.btn_registration.clicked.connect(self.open_registration_window)

        self.btn_exit = QPushButton("Закрыть", self)
        self.btn_exit.setGeometry(50, 415, 161, 31)
        self.btn_exit.clicked.connect(self.btn_exit_from_program)
        self.btn_exit.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )

    def open_login_window(self):
        self.close()
        self.login = Login(dad=self.dad, authorization=Authorization)
        self.login.show()

    def open_registration_window(self):
        self.close()
        self.registration = Registration(dad=self.dad, authorization=Authorization)
        self.registration.show()

    @staticmethod
    def btn_exit_from_program():
        sys.exit()
