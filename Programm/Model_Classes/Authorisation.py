from PyQt5.QtWidgets import QWidget, QLineEdit
from Ui_Classes import Ui_AuthorisationWindow
from PyQt5 import QtCore


class AuthorisationWindow(QWidget):
    auth_success = QtCore.pyqtSignal(int)

    def __init__(self, database):
        super().__init__()

        self.ui = Ui_AuthorisationWindow.Ui_AuthorisationWindow()
        self.ui.setupUi(self)

        self.database = database

    def authorisation_user(self):
        login = self.ui.loginLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        if not login or not password:
            self.ui.regInfoLabel.setText("Введите логин или пароль!")
            return

        user_id = self.database.check_user(login, password)

        if user_id is not None:
            self.auth_success.emit(user_id)
            self.ui.regInfoLabel.setStyleSheet("color: blue;")
            self.ui.regInfoLabel.setText("Авторизация успешна!")
        else:
            self.ui.regInfoLabel.setText("Неверный логин или пароль!")

    def show_password(self, state):
        if state:
            self.ui.passwordLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.passwordLineEdit.setEchoMode(QLineEdit.Password)

    def clear_login_password(self):
        self.ui.loginLineEdit.clear()
        self.ui.passwordLineEdit.clear()
