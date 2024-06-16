from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from Py_files.database import db
from Py_files.colors import *


class Registration(QMainWindow):
    def __init__(self, main_window=None, authorization=None):
        super().__init__()
        self.main_window = main_window
        self.authorization = authorization
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 700, 500)
        self.setWindowTitle("Регистрация")

        # Registration icon

        self.pixmap_registration = QPixmap("Images/authorization.gif")
        self.lbl_image_registration = QLabel(self)
        self.lbl_image_registration.setGeometry(30, 70, 320, 320)
        self.lbl_image_registration.setPixmap(self.pixmap_registration)

        # Registration text

        self.lbl_main = QLabel(
            "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">"
            "Дневник выполнения спортивных задач</span></p></body></html>",
            self
        )
        self.lbl_main.setGeometry(70, 40, 581, 41)

        self.lbl_registration = QLabel(
            "<html><head/><body><p><span style=\" font-size:13pt; font-weight:600;\">"
            "Регистрация аккаунта</span></p></body></html>",
            self
        )
        self.lbl_registration.setGeometry(330, 110, 261, 61)

        self.lbl_about_username = QLabel(
            "<html><head/><body><p><span style=\" font-size:10pt;\">"
            "Введите никнейм</span></p></body></html>",
            self
        )
        self.lbl_about_username.setGeometry(330, 170, 191, 20)

        self.lbl_about_password = QLabel(
            "<html><head/><body><p><span style=\" font-size:10pt;\">"
            "Введите пароль</span></p></body></html>",
            self
        )
        self.lbl_about_password.setGeometry(330, 240, 191, 20)

        # Data input

        self.usernameLE = QLineEdit(self)
        self.usernameLE.setGeometry(330, 200, 271, 22)

        self.passwordLE = QLineEdit(self)
        self.passwordLE.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordLE.setGeometry(330, 270, 271, 22)

        # Login

        self.btn_registration_and_login = QPushButton("Зарегистрироваться и войти", self)
        self.btn_registration_and_login.setGeometry(330, 300, 191, 28)
        self.btn_registration_and_login.clicked.connect(self.registration)
        self.btn_registration_and_login.setStyleSheet(light_blue_color)

        # Return to authorization

        self.btn_return_to_authorization = QPushButton("Вернуться", self)
        self.btn_return_to_authorization.setGeometry(50, 415, 161, 31)
        self.btn_return_to_authorization.clicked.connect(self.return_to_authorization)
        self.btn_return_to_authorization.setStyleSheet(light_blue_color)

        # About nickname

        self.lbl_nickname_exists = QLabel(
            "<html><head/><body><p><span style=\" font-size:9pt; color:#ff0000;\">"
            "Пользователь с таким никнеймом уже существует</span></p></body></html>",
            self
        )
        self.lbl_nickname_exists.setGeometry(200, 360, 371, 31)
        self.lbl_nickname_exists.hide()

    def registration(self) -> None:
        """ User registration: adding a user to the database """
        username = self.usernameLE.text()
        password = self.passwordLE.text()
        if username and password:
            if db.name_exists(username):
                self.lbl_nickname_exists.show()
            else:
                db.add_user(username, password)
                self.open_main_window(username, password)

    def return_to_authorization(self) -> None:
        """ Return from registration to authorization """
        self.close()
        self.authorization = self.authorization(
            main_window=self.main_window
        )
        self.authorization.show()

    def open_main_window(self, username: str, password: str) -> None:
        """ Creating a task and then opening the main window """
        user_id = db.get_user_id(username)
        self.main_window = self.main_window(user_id)
        # Fixme Убрать груду параметров ниже, привести в порядок метод .create_task() (должно быть симметрично Login)
        self.main_window.create_task(
            is_login_account=True,
            ex_main_window=self.main_window,
            parent=self,
            username=username,
            password=password
        )
