from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5 import QtCore
from Ui_Classes import Ui_ForgotPasswordWindow


class ForgotPasswordWindow(QWidget):
    closed = QtCore.pyqtSignal()

    def __init__(self, database):
        super().__init__()

        self.ui = Ui_ForgotPasswordWindow.Ui_ForgotPasswordWindow()
        self.ui.setupUi(self)

        self.database = database

    def recovery_password(self):
        login = self.ui.forgotLoginLineEdit.text()
        recovered_password = self.ui.forgotPasswordLineEdit.text()
        recovered_again_password = self.ui.forgotPasswordLineEdit2.text()
        if not login or not recovered_password:
            self.ui.forgotRegInfoLabel.setText("Введите логин или пароль!")
        elif not recovered_again_password:
            self.ui.forgotRegInfoLabel.setText("Пароли не совпадают!")
        elif self.database.recovery_password(login, recovered_password):
            self.ui.forgotRegInfoLabel.setStyleSheet("color: blue;")
            self.ui.forgotRegInfoLabel.setText("Пароль успешно изменен!")
        else:
            self.ui.forgotRegInfoLabel.setText("Пользователь с таким логином не существует!")

    def show_password(self, state):
        if state:
            self.ui.forgotPasswordLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.forgotPasswordLineEdit.setEchoMode(QLineEdit.Password)

    def show_again_password(self, state):
        if state:
            self.ui.forgotPasswordLineEdit2.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.forgotPasswordLineEdit2.setEchoMode(QLineEdit.Password)

    def clear_login_password(self):
        self.ui.forgotLoginLineEdit.clear()
        self.ui.forgotPasswordLineEdit.clear()
        self.ui.forgotPasswordLineEdit2.clear()

    def closeEvent(self, event):
        self.clear_login_password()
