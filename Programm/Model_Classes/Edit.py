from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog
from Ui_Classes import Ui_EditWindow


class EditWindow(QDialog):
    edit_right = QtCore.pyqtSignal(list)

    def __init__(self, info):
        super().__init__()

        self.ui = Ui_EditWindow.Ui_EditWindow()
        self.ui.setupUi(self)

        self.info = info

    def fill_combobox(self):
        incomes_categories = ['Зарплата', 'Премия', 'Инвестиционные доходы', 'Подарок']
        expenses_categories = ['Продукты', 'Бытовые товары', 'Оплата ЖКХ', 'Связь и интернет', 'Транспорт',
                               'Развлечения']

        if self.info[0] == 0:
            self.ui.editCombobox.addItems(incomes_categories)
            self.ui.editLineEdit.setPlaceholderText("Введите сумму дохода")
        else:
            self.ui.editCombobox.addItems(expenses_categories)

    def fill_before_info(self):
        before_info = f"{self.info[1]} {self.info[2]} {self.info[3]}"
        self.ui.editBeforeInfoLabel.setText(before_info)

    def check_fields(self):
        edit_category = self.ui.editCombobox.currentText()
        edit_amount = self.ui.editLineEdit.text()
        edit_date = self.ui.editDateEdit.text()

        try:
            float(edit_amount)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Некорректная сумма!')
            return

        if not edit_amount:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Заполните поле суммы!')
            return
        if float(edit_amount) < 0:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Сумма не может быть отрицательной!')
            return

        if self.info[0] == 0:
            flag = 0
        else:
            flag = 1

        edit_row = [flag, edit_category, edit_amount, edit_date]
        self.edit_right.emit(edit_row)

    def fix_date(self):
        current_date = QDate.currentDate()
        self.ui.editDateEdit.setDate(current_date)
