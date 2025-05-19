from datetime import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMenu, QMessageBox, QAction
from Ui_Classes import Ui_FinanceWindow


class FinanceWindow(QMainWindow):
    edit_success = QtCore.pyqtSignal(list)
    closed = QtCore.pyqtSignal()

    def __init__(self, database, user_id):
        super().__init__()

        self.ui = Ui_FinanceWindow.Ui_FinanceWindow()
        self.ui.setupUi(self)

        self.database = database
        self.user_id = user_id
        self.selected_row = -1

    def create_incomes_table(self):
        incomes_data = self.database.get_user_incomes(self.user_id)

        self.ui.incomesTableWidget.setRowCount(len(incomes_data))

        for row_number, row_data in enumerate(incomes_data):
            for column_number, column_data in enumerate(row_data):
                self.ui.incomesTableWidget.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

        self.set_table_item_flags(self.ui.incomesTableWidget)

    def create_expenses_table(self):
        expenses_data = self.database.get_user_expenses(self.user_id)

        self.ui.expensesTableWidget.setRowCount(len(expenses_data))

        for row_number, row_data in enumerate(expenses_data):
            for column_number, column_data in enumerate(row_data):
                self.ui.expensesTableWidget.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

        self.set_table_item_flags(self.ui.expensesTableWidget)

    def add_new_income(self):
        income_category = self.ui.incomesCategoryComboBox.currentText()
        income_amount = self.ui.sumIncomesLineEdit.text()
        income_date = self.ui.incomesDateEdit.text()

        self.add_new_transaction(income_category, income_amount, income_date, True)

    def add_new_expense(self):
        expense_category = self.ui.expensesCategoryComboBox.currentText()
        expense_amount = self.ui.sumExpensesLineEdit.text()
        expense_date = self.ui.expensesDateEdit.text()

        self.add_new_transaction(expense_category, expense_amount, expense_date, False)

    def add_new_transaction(self, category, amount, date, is_income):
        try:
            float(amount)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Некорректная сумма!')
            return

        if not amount:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Заполните поле суммы!')
            return
        if float(amount) < 0:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Сумма не может быть отрицательной!')
            return

        if is_income:
            table_widget = self.ui.incomesTableWidget
            add_to_database = self.database.add_income
        else:
            table_widget = self.ui.expensesTableWidget
            add_to_database = self.database.add_expense

        table_widget.insertRow(table_widget.rowCount())
        table_widget.setItem(table_widget.rowCount() - 1, 0, QTableWidgetItem(category))
        table_widget.setItem(table_widget.rowCount() - 1, 1, QTableWidgetItem(amount))
        table_widget.setItem(table_widget.rowCount() - 1, 2, QTableWidgetItem(date))

        self.set_table_item_flags(table_widget)

        add_to_database(category, amount, date, self.user_id)

    def delete_selected_row(self, table_widget):
        selected_row = table_widget.currentRow()
        category = table_widget.item(selected_row, 0).text()
        amount = table_widget.item(selected_row, 1).text()
        date = table_widget.item(selected_row, 2).text()

        table_widget.removeRow(selected_row)

        if table_widget == self.ui.incomesTableWidget:
            flag = True
            self.database.delete_transaction(category, amount, date, self.user_id, flag)
        elif table_widget == self.ui.expensesTableWidget:
            flag = False
            self.database.delete_transaction(category, amount, date, self.user_id, flag)

    def fix_date_edits(self):
        current_date = QDate.currentDate()
        for date_edit in [self.ui.incomesDateEdit, self.ui.viewSecondDateEdit, self.ui.viewSecondDateEdit_2,
                          self.ui.expensesDateEdit]:
            date_edit.setDate(current_date)
            date_edit.setMaximumDate(current_date)
        for date_edit in [self.ui.viewFirstDateEdit, self.ui.viewFirstDateEdit_2]:
            date_edit.setDate(QDate(1753, 9, 14))
            date_edit.setMaximumDate(current_date)

    def incomes_context_menu_requested(self, position):
        self.show_context_menu(position, self.ui.incomesTableWidget)

    def expenses_context_menu_requested(self, position):
        self.show_context_menu(position, self.ui.expensesTableWidget)

    def show_context_menu(self, position, table_widget):
        row_index = table_widget.indexAt(position)

        if row_index.isValid():
            context_menu = QMenu(self)
            edit_action = QAction('Редактировать', self)
            delete_action = QAction('Удалить', self)
            context_menu.addAction(edit_action)
            context_menu.addAction(delete_action)

            user_action = context_menu.exec_(table_widget.viewport().mapToGlobal(position))

            if user_action == edit_action:
                self.edit_selected_row(table_widget)
            elif user_action == delete_action:
                self.delete_selected_row(table_widget)

    def edit_selected_row(self, table_widget):
        selected_row = table_widget.currentRow()
        category = table_widget.item(selected_row, 0).text()
        amount = table_widget.item(selected_row, 1).text()
        date = table_widget.item(selected_row, 2).text()

        if table_widget == self.ui.incomesTableWidget:
            flag = 0
        else:
            flag = 1

        edit_row = [flag, category, amount, date]

        self.edit_success.emit(edit_row)

        self.selected_row = selected_row

    def update_row(self, complete_row):
        if complete_row[0] == 0:
            table_widget = self.ui.incomesTableWidget
        else:
            table_widget = self.ui.expensesTableWidget

        before_category = table_widget.item(self.selected_row, 0).text()
        before_amount = table_widget.item(self.selected_row, 1).text()
        before_date = table_widget.item(self.selected_row, 2).text()

        table_widget.setItem(self.selected_row, 0, QTableWidgetItem(complete_row[1]))
        table_widget.setItem(self.selected_row, 1, QTableWidgetItem(complete_row[2]))
        table_widget.setItem(self.selected_row, 2, QTableWidgetItem(complete_row[3]))

        if table_widget == self.ui.incomesTableWidget:
            flag = True
        else:
            flag = False

        self.database.update_transaction(self.user_id, flag, before_category, before_amount, before_date,
                                         complete_row[1], complete_row[2], complete_row[3])

        self.set_table_item_flags(table_widget)

    def get_user_name(self):
        name = self.database.give_user_name(self.user_id)
        if name is not None:
            name = name[0]
            self.ui.userInfoLabel.setText(f'Пользователь: {name}')

    def incomes_date_sort(self):
        self.tables_date_and_categories_sort(self.ui.incomesTableWidget, self.ui.sortIncomesCombobox,
                                             self.ui.viewFirstDateEdit,
                                             self.ui.viewSecondDateEdit)

    def expenses_date_sort(self):
        self.tables_date_and_categories_sort(self.ui.expensesTableWidget, self.ui.sortExpensesCombobox,
                                             self.ui.viewFirstDateEdit_2,
                                             self.ui.viewSecondDateEdit_2)

    def tables_date_and_categories_sort(self, tables_widget, combo_sort, first_date_edit, second_date_edit):
        sort_by = combo_sort.currentText()

        start_date = first_date_edit.text()
        start_date = datetime.strptime(start_date, '%d.%m.%Y')
        start_date = start_date.strftime('%Y-%m-%d')

        end_date = second_date_edit.text()
        end_date = datetime.strptime(end_date, '%d.%m.%Y')
        end_date = end_date.strftime('%Y-%m-%d')

        if tables_widget == self.ui.incomesTableWidget:
            flag = True
        elif tables_widget == self.ui.expensesTableWidget:
            flag = False
        else:
            QMessageBox.warning(self, "Ошибка", "Указана неверная таблица!")
            return

        data = []

        if sort_by == 'Дате':
            data = self.database.date_sort(self.user_id, flag, start_date, end_date)
        elif sort_by == '-':
            if tables_widget == self.ui.incomesTableWidget:
                self.create_incomes_table()
                return
            elif tables_widget == self.ui.expensesTableWidget:
                self.create_expenses_table()
                return
        else:
            data = self.database.categories_sort(self.user_id, flag, start_date, end_date, sort_by)

        if len(data) == 0:
            QMessageBox.warning(self, "Ошибка", "Данных за указанный период нет!")
            return

        tables_widget.setRowCount(len(data))
        for row_number, row_data in enumerate(data):
            for column_number, column_data in enumerate(row_data):
                tables_widget.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

        self.set_table_item_flags(tables_widget)

    def set_table_item_flags(self, table_widget):
        rows = table_widget.rowCount()
        cols = table_widget.columnCount()
        for row in range(rows):
            for col in range(cols):
                item = table_widget.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def closeEvent(self, event):
        self.closed.emit()
