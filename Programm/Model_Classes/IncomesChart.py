from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChartView, QPieSeries, QPieSlice, QChart
from datetime import datetime
from Ui_Classes import Ui_incomesChart


class IncomesWindow(QWidget):
    def __init__(self, database, user_id, flag):
        super().__init__()

        self.ui = Ui_incomesChart.Ui_incomesChart()
        self.ui.setupUi(self)
        self.database = database
        self.user_id = user_id
        self.flag = flag

    def fix_date_edits(self):
        current_date = QDate.currentDate()
        self.ui.chartFirstDateEdit.setDate(QDate(1753, 9, 14))
        self.ui.chartFirstDateEdit.setMaximumDate(current_date)

        self.ui.chartSecondDateEdit.setDate(current_date)
        self.ui.chartSecondDateEdit.setMaximumDate(current_date)

    def send_date(self):
        self.create_chart(self.ui.chartFirstDateEdit, self.ui.chartSecondDateEdit)

    def create_chart(self, first_date, second_date):
        start_date = first_date.text()
        start_date = datetime.strptime(start_date, '%d.%m.%Y')
        start_date = start_date.strftime('%Y-%m-%d')

        end_date = second_date.text()
        end_date = datetime.strptime(end_date, '%d.%m.%Y')
        end_date = end_date.strftime('%Y-%m-%d')

        data = self.database.chart_categories(self.user_id, start_date, end_date, self.flag)

        total_amount = sum(amount for category, amount in data)

        series = QPieSeries()

        colors = [Qt.red, Qt.green, Qt.blue, Qt.magenta, Qt.cyan, Qt.gray]

        for i, (category, amount) in enumerate(data):
            slice = QPieSlice(category, amount)
            slice.setLabel(f"{category}: {amount}")
            slice.setBrush(colors[i % len(colors)])
            series.append(slice)
            series.setLabelsVisible()

        chart_view = QChartView()
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.chart().addSeries(series)
        if self.flag:
            chart_view.chart().setTitle("Круговая диаграмма доходов")
        else:
            chart_view.chart().setTitle("Круговая диаграмма расходов")
        chart_view.chart().setTitleFont(QtGui.QFont("Open Sans Condensed SemiBold", 14))

        for slice in series.slices():
            slice.setLabelFont(QtGui.QFont("Open Sans Condensed SemiBold", 14))

        chart_view.chart().setTheme(QChart.ChartThemeLight)
        chart_view.chart().legend().setVisible(True)
        chart_view.chart().legend().setAlignment(Qt.AlignBottom)
        chart_view.chart().legend().setFont(QtGui.QFont("Open Sans Condensed SemiBold", 14))

        total_label = QLabel(self.ui.incomesGraphicsView)
        total_label.setFont(QtGui.QFont("Open Sans Condensed SemiBold", 12))
        if self.flag:
            total_label.setText(f"Общая сумма доходов за указанный период: {total_amount:.2f} руб.")
        else:
            total_label.setText(f"Общая сумма расходов за указанный период: {total_amount:.2f} руб.")
        total_label.setGeometry(QtCore.QRect(10, 10, 400, 30))

        # Устанавливаем представление графика на графический виджет
        graphics_view = self.ui.incomesGraphicsView
        graphics_view.setChart(chart_view.chart())
