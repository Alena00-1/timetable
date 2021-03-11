import hashlib
import os
import re

from PyQt5.QtWidgets import QDialog

import resourses.authorization as authorization


class Authorization(QDialog, authorization.Ui_Dialog):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller
        self.controller.set_authorization(self)
        self.pushButton.clicked.connect(self.controller.push_button_login)
        self.pushButton_2.clicked.connect(self.controller.push_button_add_user)
        self.reset()

    def check_login(self, data, new_pass):
        self.reset()
        if not data:
            self.label_4.setVisible(True)
            self.label_4.setText('Неверный логин!')
            return False
        key = data[0][1]
        salt = data[0][2]
        a, new_key = self.hash_password(new_pass, bytearray.fromhex(salt))
        if new_key == key:
            self.controller.status = int(data[0][3])
            return True
        else:
            self.label_5.setVisible(True)
            self.label_5.setText('Неверный пароль!')
            return False

    def check_empty(self):
        self.reset()
        a = None
        b = None
        if not self.lineEdit.text().strip(' '):
            self.label_4.setVisible(True)
            self.label_4.setText('Необходимо заполнить поле!')
        else:
            a = self.lineEdit.text().strip(' ')
        if not self.lineEdit_2.text().strip(' '):
            self.label_5.setVisible(True)
            self.label_5.setText('Необходимо заполнить поле!')
        else:
            b = self.lineEdit_2.text().strip(' ')
        return a, b

    def hash_password(self, password, salt=os.urandom(32)):
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return str(salt.hex()), str(key.hex())

    def reset(self):
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_4.setStyleSheet('color: red')
        self.label_5.setStyleSheet('color: red')

    def validate_login(self, login):
        reg = r'[a-z]{5,}[_-]*[a-z]*'
        if re.fullmatch(reg, login):
            return True
        return False
