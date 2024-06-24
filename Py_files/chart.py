from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtWidgets import QWidget, QFileDialog
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pandas.core.series import Series
from math import ceil


class Chart(QMainWindow):
    def __init__(self, points: Series, task_name: str, result_name: str, ex_main_window=None):
        super().__init__()
        self.points = points
        self.task_name = task_name
        self.result_name = result_name
        self.ex_main_window = ex_main_window
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle("График результатов")
        self.setGeometry(100, 100, 800, 600)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.chartLayout = QVBoxLayout()
        self.chartLayout.addWidget(self.canvas)

        chartWidget = QWidget()
        chartWidget.setLayout(self.chartLayout)
        self.setCentralWidget(chartWidget)

        self.draw_chart()

    def draw_chart(self) -> None:
        """ Creating a chart and drawing it """
        ax = self.figure.subplots()
        ax.plot(
            self.points.index,
            self.points.values,
            marker='o',
            color='blue',
            linestyle='--',
            linewidth=2,
        )
        ax.set(
            xlabel="Дата",
            ylabel=self.result_name,
            title=self.task_name
        )
        ax.grid()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=ceil(len(self.points) / 10)))
        plt.gcf().autofmt_xdate()
        self.canvas.draw()

    def show_chart(self) -> None:
        self.show()

    def download_chart(self) -> None:
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
