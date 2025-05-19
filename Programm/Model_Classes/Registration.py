from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLineEdit
from Ui_Classes import Ui_RegistrationWindow


class RegistrationWindow(QWidget):
    closed = QtCore.pyqtSignal()

    def __init__(self, database):
        super().__init__()
        self.ui = Ui_RegistrationWindow.Ui_RegistrationWindow()
        self.ui.setupUi(self)

        self.database = database

    def registration_user(self):
        new_login = self.ui.newLoginLineEdit.text()
        new_password = self.ui.newPasswordLineEdit.text()
        again_password = self.ui.newPasswordLineEdit2.text()

        if not new_login or not new_password:
            self.ui.newRegInfoLabel.setText("Введите логин или пароль!")
        elif not again_password:
            self.ui.newRegInfoLabel.setText("Пароли не совпадают!")
        elif self.database.register_user(new_login, new_password):
            self.ui.newRegInfoLabel.setStyleSheet("color: blue;")
            self.ui.newRegInfoLabel.setText("Регистрация успешна!")
        else:
            self.ui.newRegInfoLabel.setText("Пользователь с таким логином уже существует!")

    def show_password(self, state):
        if state:
            self.ui.newPasswordLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.newPasswordLineEdit.setEchoMode(QLineEdit.Password)

    def show_again_password(self, state):
        if state:
            self.ui.newPasswordLineEdit2.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.newPasswordLineEdit2.setEchoMode(QLineEdit.Password)

    def clear_login_password(self):
        self.ui.newLoginLineEdit.clear()
        self.ui.newPasswordLineEdit.clear()
        self.ui.newPasswordLineEdit2.clear()

    def closeEvent(self, event):
        self.clear_login_password()


