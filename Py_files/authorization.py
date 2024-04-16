import sys
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from Py_files.database import db
from Py_files.main_window import MainWindow


# Класс для работы с окном: авторизация пользователя
class Authorization(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.login = Login()
        self.login.show()

    def open_registration_window(self):
        self.close()
        self.registration = Registration()
        self.registration.show()

    @staticmethod
    def btn_exit_from_program():
        sys.exit()


# Класс для работы с окном: вход пользователя в аккаунт
class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 700, 500)
        self.setWindowTitle("Вход в аккаунт")

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

        self.info_about_username = QLabel('<html><head/><body><p><span style=" font-size:10pt;">'
                                          'Введите никнейм</span></p></body></html>', self)
        self.info_about_username.setGeometry(330, 170, 191, 20)

        self.username = QLineEdit(self)
        self.username.setGeometry(330, 200, 271, 22)

        self.info_about_password = QLabel('<html><head/><body><p><span style=" font-size:10pt;">'
                                          'Введите пароль</span></p></body></html>', self)
        self.info_about_password.setGeometry(330, 240, 191, 20)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setGeometry(330, 270, 271, 22)

        self.btn_login_account = QPushButton("Войти", self)
        self.btn_login_account.setGeometry(330, 310, 161, 28)
        self.btn_login_account.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )
        self.btn_login_account.clicked.connect(self.login_account)

        self.user_not_exists = QLabel("<html><head/><body><p><span style=\" font-size:10pt; color:#ff3613;\">"
                                      "Пользователя не существует</span></p></body></html>", self)
        self.user_not_exists.setGeometry(300, 360, 261, 51)
        self.user_not_exists.hide()

        self.back_authorization = QPushButton("Вернуться", self)
        self.back_authorization.setGeometry(50, 415, 161, 31)
        self.back_authorization.clicked.connect(self.back_window_authorization)
        self.back_authorization.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )

    def login_account(self):
        username = self.username.text()
        password = self.password.text()
        if username and password:
            if db.person_exists(username, password):
                self.open_main_window(username)
            else:
                self.user_not_exists.show()

    def back_window_authorization(self):
        self.close()
        self.authorization = Authorization()
        self.authorization.show()

    def open_main_window(self, username):
        self.close()
        self.id_person = db.get_id_person(username)
        self.ex = MainWindow(self.id_person, dad=Authorization)
        self.ex.show()


# Класс для работы с окном: регистрация пользователя
class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 700, 500)
        self.setWindowTitle("Регистрация")

        self.pixmap_authorization = QPixmap("Images/authorization.gif")
        self.image_authorization = QLabel(self)
        self.image_authorization.move(30, 70)
        self.image_authorization.resize(320, 320)
        self.image_authorization.setPixmap(self.pixmap_authorization)

        self.main_title = QLabel("<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">"
                                 "Дневник выполнения спортивных задач</span></p></body></html>", self)
        self.main_title.setGeometry(70, 40, 581, 41)

        self.title_authorization = QLabel('<html><head/><body><p><span style=" font-size:13pt; font-weight:600;">'
                                          'Регистрация аккаунта</span></p></body></html>', self)
        self.title_authorization.setGeometry(330, 110, 261, 61)

        self.info_about_username = QLabel('<html><head/><body><p><span style=" font-size:10pt;">'
                                          'Введите никнейм</span></p></body></html>', self)
        self.info_about_username.setGeometry(330, 170, 191, 20)

        self.username = QLineEdit(self)
        self.username.setGeometry(330, 200, 271, 22)

        self.info_about_password = QLabel('<html><head/><body><p><span style=" font-size:10pt;">'
                                          'Введите пароль</span></p></body></html>', self)
        self.info_about_password.setGeometry(330, 240, 191, 20)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setGeometry(330, 270, 271, 22)

        self.btn_registration_and_login = QPushButton("Зарегистрироваться и войти", self)
        self.btn_registration_and_login.setGeometry(330, 300, 191, 28)
        self.btn_registration_and_login.clicked.connect(self.registration_account)
        self.btn_registration_and_login.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )

        self.back_authorization = QPushButton("Вернуться", self)
        self.back_authorization.setGeometry(50, 415, 161, 31)
        self.back_authorization.clicked.connect(self.back_window_authorization)
        self.back_authorization.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )
        self.nickname_exists = QLabel("<html><head/><body><p><span style=\" font-size:9pt; color:#ff0000;\">"
                                      "Пользователь с таким никнеймом уже существует</span></p></body></html>", self)
        self.nickname_exists.setGeometry(200, 360, 371, 31)
        self.nickname_exists.hide()

    def registration_account(self):
        username = self.username.text()
        password = self.password.text()
        if username and password:
            if db.name_exists(username):
                self.nickname_exists.show()
            else:
                db.set_person(username, password)
                self.open_main_window(username, password)

    def back_window_authorization(self):
        self.close()
        self.authorization = Authorization()
        self.authorization.show()

    def open_main_window(self, username, password):
        self.id_person = db.get_id_person(username)
        self.ex = MainWindow(self.id_person, dad=Authorization)
        self.ex.create_new_task(
            is_login_account=True,
            ex_main_window=self.ex,
            parent=self,
            username=username,
            password=password
        )
