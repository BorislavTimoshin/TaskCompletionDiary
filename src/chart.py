import math

import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from src.database import db


class Chart(QMainWindow):
    def __init__(self, ex_main_window, points: pd.Series, translations: dict):
        super().__init__()
        uic.loadUi(f"Design/{ex_main_window.current_language}/chart.ui", self)
        self.ex_main_window = ex_main_window
        self.points = points
        self.translations = translations
        self.task_name = ex_main_window.CB_tasks.currentText()
        self.current_language = ex_main_window.current_language
        self.user_id = ex_main_window.user_id
        self.initUI()

    def initUI(self) -> None:
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Adding a chart to chartWidgetLayout
        self.chartWidgetLayout.addWidget(self.canvas)

    def get_result_name_on_chart(self, task_name: str) -> str:
        """Getting the name of the result that will be displayed in the graph"""
        result_name, unit = db.get_task(task_name, self.user_id)
        if unit == "number":
            return result_name
        if unit == "time":
            return f"{result_name} (с)"
        unit_abbr = self.translations[self.current_language]["unit"][unit]
        return f"{result_name} ({unit_abbr})"

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
        result_name = self.get_result_name_on_chart(self.task_name)
        date_title = self.translations[self.current_language]["tableWidget"]["date"]
        ax.set(xlabel=date_title, ylabel=result_name, title=self.task_name)
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


