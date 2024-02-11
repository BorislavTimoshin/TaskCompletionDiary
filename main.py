import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from Py_files.authorization import Authorization

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex_authorization = Authorization()
    ex_authorization.show()
    sys.exit(app.exec())
