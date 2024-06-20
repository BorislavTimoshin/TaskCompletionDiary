from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from Py_files.database import db
from Py_files.colors import light_blue_color


class Login(QMainWindow):
    def __init__(self, main_window=None, authorization=None):
        super().__init__()
        self.main_window = main_window
        self.authorization = authorization
        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(600, 200, 700, 500)
        self.setWindowTitle("Вход в аккаунт")

        # Login icon

        self.pixmap_login = QPixmap("Images/authorization.gif")
        self.lbl_image_login = QLabel(self)
        self.lbl_image_login.setGeometry(30, 70, 320, 320)
        self.lbl_image_login.setPixmap(self.pixmap_login)

        # Login text

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

        self.LE_username = QLineEdit(self)
        self.LE_username.setGeometry(330, 200, 271, 22)

        self.LE_password = QLineEdit(self)
        self.LE_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.LE_password.setGeometry(330, 270, 271, 22)

        # Login

        self.btn_login = QPushButton("Войти", self)
        self.btn_login.setGeometry(330, 310, 161, 28)
        self.btn_login.setStyleSheet(light_blue_color)
        self.btn_login.clicked.connect(self.login)

        # Return to authorization

        self.btn_return_to_authorization = QPushButton("Вернуться", self)
        self.btn_return_to_authorization.setGeometry(50, 415, 161, 31)
        self.btn_return_to_authorization.clicked.connect(self.return_to_authorization)
        self.btn_return_to_authorization.setStyleSheet(light_blue_color)

        # About user

        self.lbl_user_not_exists = QLabel(
            "<html><head/><body><p><span style=\" font-size:10pt; color:#ff3613;\">"
            "Пользователя не существует</span></p></body></html>",
            self
        )
        self.lbl_user_not_exists.setGeometry(300, 360, 261, 51)
        self.lbl_user_not_exists.hide()

    def login(self) -> None:
        username = self.LE_username.text()
        password = self.LE_password.text()
        if username and password:
            if db.user_exists(username, password):
                user_id = db.get_user_id(username)
                self.open_main_window(user_id)
            else:
                self.lbl_user_not_exists.show()

    def return_to_authorization(self) -> None:
        """ Return from login to authorization """
        self.close()
        self.authorization = self.authorization(
            main_window=self.main_window
        )
        self.authorization.show()

    def open_main_window(self, user_id: int) -> None:
        self.close()
        self.ex_main_window = self.main_window(user_id)
        self.ex_main_window.show()
