from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFileDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from math import ceil


class Chart(QMainWindow):
    def __init__(self, parent, values, label_result):
        super().__init__(parent)

        self.values = values
        self.label_result = label_result

        self.setWindowTitle("График результатов")
        self.setGeometry(100, 100, 800, 600)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.show_chart()

    def show_chart(self):
        ax = self.figure.add_subplot(111)
        ax.plot(
            self.values.index,
            self.values.values,
            color='blue',
            linestyle='--',
            linewidth=2,
        )
        ax.set(
            xlabel="Дата",
            ylabel=self.label_result,
            title="График результатов"
        )
        ax.grid()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=ceil(len(self.values) / 10)))
        plt.gcf().autofmt_xdate()
        self.canvas.draw()

    def download_chart(self):
        file_path, file_type = QFileDialog.getSaveFileName(
            self,
            'Скачать график',
            '',
            '.jpg;;.jpeg;;.png'
        )
        if not file_path:
            return
        if file_type == ".jpg":
            plt.savefig(f"{file_path}.jpg", bbox_inches='tight')
        elif file_type == ".jpeg":
            plt.savefig(f"{file_path}.jpeg", bbox_inches='tight')
        elif file_type == ".png":
            plt.savefig(f"{file_path}.png", bbox_inches='tight')
