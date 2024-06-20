from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QPlainTextEdit, QLabel
from PyQt5.QtGui import QPixmap


class AboutProgram(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("О программе")
        self.setGeometry(650, 300, 610, 400)

        about_program_btns = QDialogButtonBox(QDialogButtonBox.Ok, self)
        about_program_btns.accepted.connect(self.accept)
        about_program_btns.move(440, 360)

        self.pixmap_book = QPixmap("Images/book.png")
        self.lbl_book = QLabel(self)
        self.lbl_book.setGeometry(18, 85, 200, 218)
        self.lbl_book.setPixmap(self.pixmap_book)

    def program_description(self):
        with open("Other_files/program_description.txt", "r", encoding="utf-8") as file:
            program_description_text = file.read()

        self.PLE_program_description = QPlainTextEdit(program_description_text, self)
        self.PLE_program_description.setGeometry(230, 40, 351, 301)
        self.PLE_program_description.setReadOnly(True)
        self.show()

    def program_version(self):
        with open("Other_files/program_version.txt", "r", encoding="utf-8") as file:
            program_version_text = file.read()

        self.PLE_program_version = QPlainTextEdit(program_version_text, self)
        self.PLE_program_version.setGeometry(230, 40, 351, 301)
        self.PLE_program_version.setReadOnly(True)
        self.show()


def get_number_of_records_for_plotting(parent):
    if parent.plotting_option_1.isChecked():
        return 30
    if parent.plotting_option_2.isChecked():
        return 60
    if parent.plotting_option_3.isChecked():
        return 90
    if parent.plotting_option_4.isChecked():
        return 120
    if parent.plotting_option_5.isChecked():
        return 150
    if parent.plotting_option_6.isChecked():
        return 180
    if parent.plotting_option_7.isChecked():
        return 270
    if parent.plotting_option_8.isChecked():
        return 365
    if parent.plotting_option_9.isChecked():
        return 730
    return "all_records"
