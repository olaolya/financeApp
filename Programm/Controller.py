import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLineEdit
from Model_Classes.FinanceDb import FinanceDb
from Model_Classes.Authorisation import AuthorisationWindow
from Model_Classes.Registration import RegistrationWindow
from Model_Classes.ForgotPassword import ForgotPasswordWindow
from Model_Classes.Finance import FinanceWindow
from Model_Classes.Edit import EditWindow
from Model_Classes.IncomesChart import IncomesWindow


class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.database = FinanceDb("finance.db")
        self.database.create_tables()
        self.authorisation_window = None
        self.registration_window = None
        self.forgot_password_window = None
        self.finance_window = None
        self.edit_dialog = None
        self.incomes_chart = None
        self.user_id = None
        self.info = None

    def run_authorisation_window(self):
        if not self.authorisation_window:
            self.authorisation_window = AuthorisationWindow(self.database)
            self.authorisation_window.show()

            # Настройка сигналов и слотов для элементов интерфейса
            self.authorisation_window.ui.authorisationButton.clicked.connect(self.
                                                                             authorisation_window.authorisation_user)
            self.authorisation_window.ui.registrationButton.clicked.connect(self.
                                                                            authorisation_window.clear_login_password)
            self.authorisation_window.ui.forgotPasswordButton.clicked.connect(self.
                                                                              authorisation_window.clear_login_password)
            self.authorisation_window.ui.passwordCheckBox.stateChanged.connect(self.
                                                                               authorisation_window.show_password)
            self.authorisation_window.ui.passwordCheckBox.setChecked(False)
            self.authorisation_window.ui.passwordLineEdit.setEchoMode(QLineEdit.Password)

            self.authorisation_window.ui.registrationButton.clicked.connect(self.run_registration_window)
            self.authorisation_window.ui.forgotPasswordButton.clicked.connect(self.run_forgot_password_window)
            self.authorisation_window.auth_success.connect(self.on_authorisation_success)

    def run_registration_window(self):
        self.registration_window = RegistrationWindow(self.database)
        self.registration_window.show()

        # Настройка сигналов и слотов для элементов интерфейса
        self.registration_window.ui.newRegistrationButton.clicked.connect(self.
                                                                              registration_window.registration_user)
        self.registration_window.ui.newPasswordCheckBox.stateChanged.connect(self.registration_window.show_password)
        self.registration_window.ui.newPasswordCheckBox2.stateChanged.connect(
            self.registration_window.show_again_password)
        self.registration_window.ui.newPasswordCheckBox.setChecked(False)
        self.registration_window.ui.newPasswordLineEdit.setEchoMode(QLineEdit.Password)
        self.registration_window.ui.newPasswordCheckBox2.setChecked(False)
        self.registration_window.ui.newPasswordLineEdit2.setEchoMode(QLineEdit.Password)

        self.registration_window.closed.connect(self.on_registration_window_closed)

    def run_forgot_password_window(self):
        self.forgot_password_window = ForgotPasswordWindow(self.database)
        self.forgot_password_window.show()

        # Настройка сигналов и слотов для элементов интерфейса
        self.forgot_password_window.ui.forgotPasswordButton.clicked.connect(
            self.forgot_password_window.recovery_password)
        self.forgot_password_window.ui.forgotPasswordCheckBox.stateChanged.connect(
            self.forgot_password_window.show_password)
        self.forgot_password_window.ui.forgotPasswordCheckBox2.stateChanged.connect(
            self.forgot_password_window.show_again_password)
        self.forgot_password_window.ui.forgotPasswordCheckBox.setChecked(False)
        self.forgot_password_window.ui.forgotPasswordLineEdit.setEchoMode(QLineEdit.Password)
        self.forgot_password_window.ui.forgotPasswordCheckBox2.setChecked(False)
        self.forgot_password_window.ui.forgotPasswordLineEdit2.setEchoMode(QLineEdit.Password)

        self.forgot_password_window.closed.connect(self.on_forgot_password_window)

    def on_authorisation_success(self, user_id):
        self.user_id = user_id
        self.finance_window = FinanceWindow(self.database, user_id=self.user_id)
        self.finance_window.edit_success.connect(self.on_edit_dialog)
        self.finance_window.show()
        self.authorisation_window.close()

        # Настройка сигналов и слотов для элементов интерфейса
        self.finance_window.create_incomes_table()
        self.finance_window.create_expenses_table()
        self.finance_window.fix_date_edits()
        self.finance_window.get_user_name()

        self.finance_window.ui.saveIncomesButton.clicked.connect(self.finance_window.add_new_income)
        self.finance_window.ui.saveExpensesButton.clicked.connect(self.finance_window.add_new_expense)

        self.finance_window.ui.incomesTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.finance_window.ui.incomesTableWidget.customContextMenuRequested.connect(
            self.finance_window.incomes_context_menu_requested)

        self.finance_window.ui.expensesTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.finance_window.ui.expensesTableWidget.customContextMenuRequested.connect(
            self.finance_window.expenses_context_menu_requested)

        self.finance_window.ui.sortIncomesCombobox.currentIndexChanged.connect(self.finance_window.incomes_date_sort)
        self.finance_window.ui.sortExpensesCombobox.currentIndexChanged.connect(self.finance_window.expenses_date_sort)

        self.finance_window.ui.viewFirstDateEdit.dateChanged.connect(self.finance_window.incomes_date_sort)
        self.finance_window.ui.viewSecondDateEdit.dateChanged.connect(self.finance_window.incomes_date_sort)

        self.finance_window.ui.viewFirstDateEdit_2.dateChanged.connect(self.finance_window.expenses_date_sort)
        self.finance_window.ui.viewSecondDateEdit_2.dateChanged.connect(self.finance_window.expenses_date_sort)

        self.finance_window.ui.openIncomesDiagrammButton.clicked.connect(
            lambda: self.run_incomes_chart(user_id, flag=True))
        self.finance_window.ui.openExpensesDiagrammButton.clicked.connect(
            lambda: self.run_incomes_chart(user_id, flag=False))
        self.finance_window.closed.connect(self.on_finance_window_closed)

    def run_incomes_chart(self, user_id, flag):
        self.incomes_chart = IncomesWindow(self.database, user_id, flag)
        self.incomes_chart.show()

        # Настройка сигналов и слотов для элементов интерфейса
        self.incomes_chart.ui.chartFirstDateEdit.dateChanged.connect(self.incomes_chart.send_date)
        self.incomes_chart.ui.chartSecondDateEdit.dateChanged.connect(self.incomes_chart.send_date)
        self.incomes_chart.fix_date_edits()

    def on_edit_dialog(self, info):
        self.info = info
        self.edit_dialog = EditWindow(info=self.info)
        self.edit_dialog.show()

        # Настройка сигналов и слотов для элементов интерфейса
        self.edit_dialog.fill_combobox()
        self.edit_dialog.fill_before_info()
        self.edit_dialog.fix_date()
        self.edit_dialog.ui.editButtonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('Сохранить')
        self.edit_dialog.ui.editButtonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText('Отменить')
        self.edit_dialog.ui.editButtonBox.accepted.connect(self.edit_dialog.check_fields)

        self.edit_dialog.edit_right.connect(self.on_edit_right)

    def on_edit_right(self, complete_row):
        if self.finance_window.isVisible():
            self.finance_window.update_row(complete_row)

    def on_registration_window_closed(self):
        self.registration_window = None
        if not self.authorisation_window:
            self.switch_to_authorisation_window()
        if not self.registration_window:
            self.app.quit()

    def on_forgot_password_window(self):
        self.forgot_password_window = None
        if not self.authorisation_window:
            self.switch_to_authorisation_window()
        if not self.forgot_password_window:
            self.app.quit()

    def switch_to_authorisation_window(self):
        if self.registration_window:
            self.registration_window.hide()
        if self.authorisation_window:
            self.authorisation_window.show()

    def switch_to_registration_window(self):
        if self.authorisation_window:
            self.authorisation_window.hide()
        if self.registration_window:
            self.registration_window.show()

    def start(self):
        self.run_authorisation_window()
        sys.exit(self.app.exec())

    def on_finance_window_closed(self):
        self.app.quit()


if __name__ == "__main__":
    controller = Controller()
    controller.start()
