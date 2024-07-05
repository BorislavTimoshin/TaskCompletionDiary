import math

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pandas.core.series import Series
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow


class Chart(QMainWindow):
    def __init__(self, ex_main_window, points: Series, task_name: str, result_name: str, translations: dict):
        super().__init__()
        self.current_language = ex_main_window.current_language
        uic.loadUi(f"Design/{self.current_language}/chart.ui", self)
        self.ex_main_window = ex_main_window
        self.points = points
        self.task_name = task_name
        self.result_name = result_name
        self.translations = translations
        self.initUI()

    def initUI(self) -> None:
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Adding a chart to chartWidgetLayout
        self.chartWidgetLayout.addWidget(self.canvas)

    def draw_chart(self) -> None:
        """Creating a chart and drawing it"""
        ax = self.figure.subplots()
        ax.plot(
            self.points.index,
            self.points.values,
            marker="o",
            color="blue",
            linestyle="--",
            linewidth=2,
        )
        date_title = self.translations[self.current_language]["tableWidget"]["date"]
        ax.set(xlabel=date_title, ylabel=self.result_name, title=self.task_name)
        ax.grid()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%y"))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=math.ceil(len(self.points) / 10)))
        plt.gcf().autofmt_xdate()
        self.canvas.draw()

    def show_chart(self) -> None:
        self.draw_chart()
        self.show()

    def download_chart(self) -> None:
        self.draw_chart()
        download_chart_title = self.translations[self.current_language]["title"]["downloadChart"]
        file_path, file_type = QFileDialog.getSaveFileName(
            self,
            download_chart_title,
            "",
            ".jpg;;.jpeg;;.png",
        )
        if not file_path:
            return
        if file_type == ".jpg":
            plt.savefig(f"{file_path}.jpg", bbox_inches="tight")
        elif file_type == ".jpeg":
            plt.savefig(f"{file_path}.jpeg", bbox_inches="tight")
        elif file_type == ".png":
            plt.savefig(f"{file_path}.png", bbox_inches="tight")
