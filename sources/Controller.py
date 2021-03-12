import os

from PyQt5.QtCore import QObject

from sources.database import *


class Controller(QObject):
    def __init__(self):
        super().__init__()
        self.path = os.getcwd()
        self.connect_DB = DataBase(connect_database(os.path.join(self.path, 'timetable.db')))
        self.set_settings()
        self.status = int()
        self.account = list()

    def set_timeTable(self, mainWin):
        self.mainWin = mainWin

    def set_builder(self, builder):
        self.builder = builder

    def set_authorization(self, authorization):
        self.authorization = authorization

    def set_settings(self):
        self.connect_DB.create_table_subject()
        self.connect_DB.create_table_lecturer()
        self.connect_DB.create_table_classroom()
        self.connect_DB.create_table_groups()
        self.connect_DB.create_table_timetable()
        self.connect_DB.create_table_users()

    def push_button_add_row(self):
        row = self.mainWin.tableWidget.currentIndex().row()
        self.mainWin.tableWidget.insertRow(row)
        self.builder.set_line_edit(self.mainWin.tableWidget, row)
        self.builder.set_button(self.mainWin.tableWidget, row)
        combo_lecturer, combo_subject, combo_classroom = self.builder.set_combo_box(self.mainWin.tableWidget, row)
        self.set_combobox(combo_lecturer, combo_subject, combo_classroom)

    def set_combobox(self, combo_lecturer, combo_subject, combo_classroom):
        self.set_lecturer(0, combo_lecturer)
        if combo_lecturer.count() < 1:
            self.mainWin.message_error_lecturer()
            self.push_button_remove_row(1)
            return
        self.set_subject(0, combo_subject)
        if combo_subject.count() < 1:
            self.mainWin.message_error_subject()
            self.push_button_remove_row(1)
            return
        self.set_classroom(0, combo_classroom)
        if combo_classroom.count() < 1:
            self.mainWin.message_error_classroom()
            self.push_button_remove_row(1)
            return

    def push_button_remove_row(self, count):
        self.builder.remove_row(self.mainWin.tableWidget, count)

    def push_button_add_subject(self):
        data = self.mainWin.edit_subject.text().strip()
        if data:
            self.mainWin.edit_subject.setStyleSheet('')
            self.connect_DB.insert_into_subject(data)
        else:
            self.mainWin.empty_value(self.mainWin.edit_subject)
            return
        self.mainWin.edit_subject.clear()
        self.mainWin.tableWidget.setRowCount(0)
        self.mainWin.table_subject.setRowCount(0)
        self.set_groups(0)
        self.set_subject(1)

    def push_button_add_lecturer(self):
        data = self.mainWin.edit_lecturer.text().strip()
        if data:
            self.mainWin.edit_lecturer.setStyleSheet('')
            self.connect_DB.insert_into_lecturer(data)
        else:
            self.mainWin.empty_value(self.mainWin.edit_lecturer)
            return
        self.mainWin.edit_lecturer.clear()
        self.mainWin.tableWidget.setRowCount(0)
        self.mainWin.table_lecturer.setRowCount(0)
        self.set_groups(0)
        self.set_lecturer(1)

    def push_button_add_classroom(self):
        data = self.mainWin.edit_classroom.text().strip()
        if data:
            self.mainWin.edit_classroom.setStyleSheet('')
            self.connect_DB.insert_into_classroom(data)
        else:
            self.mainWin.empty_value(self.mainWin.edit_classroom)
            return
        self.mainWin.edit_classroom.clear()
        self.mainWin.tableWidget.setRowCount(0)
        self.mainWin.table_classroom.setRowCount(0)
        self.set_groups(0)
        self.set_classroom(1)

    def push_button_add_group(self):
        data = self.mainWin.edit_group.text().strip()
        if data:
            self.mainWin.edit_group.setStyleSheet('')
            self.connect_DB.insert_into_groups(data)
        else:
            self.mainWin.empty_value(self.mainWin.edit_group)
            return
        self.mainWin.edit_group.clear()
        self.mainWin.tableWidget.setRowCount(0)
        self.mainWin.table_groups.setRowCount(0)
        self.push_button_update_table()

    def push_button_delete_group(self):
        row = self.mainWin.table_groups.currentIndex().row()
        name_group = self.mainWin.table_groups.item(row, 0)
        self.connect_DB.delete_from_groups(name_group.text())
        self.mainWin.tableWidget.setRowCount(0)
        self.mainWin.table_groups.setRowCount(0)
        self.push_button_update_table()

    def push_button_delete_lecturer(self):
        row = self.mainWin.table_lecturer.currentIndex().row()
        lecturer_SNP = self.mainWin.table_lecturer.item(row, 0)
        self.connect_DB.delete_from_lecturer(lecturer_SNP.text())
        self.mainWin.tableWidget.setRowCount(0)
        self.mainWin.table_lecturer.setRowCount(0)
        self.set_lecturer(1)
        self.set_groups(0)

    def push_button_delete_subject(self):
        row = self.mainWin.table_subject.currentIndex().row()
        subject_name = self.mainWin.table_subject.item(row, 0)
        self.connect_DB.delete_from_subject(subject_name.text())
        self.mainWin.tableWidget.setRowCount(0)
        self.mainWin.table_subject.setRowCount(0)
        self.set_subject(1)
        self.set_groups(0)

    def push_button_delete_classroom(self):
        row = self.mainWin.table_classroom.currentIndex().row()
        classroom_number = self.mainWin.table_classroom.item(row, 0)
        self.connect_DB.delete_from_classroom(classroom_number.text())
        self.mainWin.tableWidget.setRowCount(0)
        self.mainWin.table_classroom.setRowCount(0)
        self.set_classroom(1)
        self.set_groups(0)

    def push_button_delete_user(self):
        row = self.mainWin.table_user.currentIndex().row()
        login_user = self.mainWin.table_user.item(row, 0)
        self.connect_DB.delete_from_user(login_user.text())
        self.mainWin.table_user.setRowCount(0)
        self.set_users()

    def push_button_save(self):
        self.connect_DB.delete_from_timetable((self.mainWin.dateEdit.date()).toPyDate())
        self.mainWin.create_table()

    def push_button_update_table(self):
        index = self.mainWin.tabWidget_2.currentIndex()
        table = [self.mainWin.table_lecturer, self.mainWin.table_subject, self.mainWin.table_classroom,
                 self.mainWin.table_user, self.mainWin.tableWidget, self.mainWin.table_groups]
        for i in table:
            i.setRowCount(0)
        self.set_lecturer(1)
        self.set_subject(1)
        self.set_classroom(1)
        self.set_users()
        if self.set_groups(1):
            self.set_groups(0)
            self.mainWin.pushButton.setVisible(True)
        else:
            self.mainWin.pushButton.setVisible(False)
        if self.status != 1:
            self.mainWin.settings_for_user()
        self.mainWin.clear_mask()
        self.mainWin.tabWidget_2.setCurrentIndex(index)

    def push_button_delete(self, table):
        if table.objectName() == 'table_classroom':
            self.push_button_delete_classroom()
        elif table.objectName() == 'table_groups':
            self.push_button_delete_group()
        elif table.objectName() == 'table_lecturer':
            self.push_button_delete_lecturer()
        elif table.objectName() == 'table_subject':
            self.push_button_delete_subject()
        else:
            self.push_button_delete_user()

    def push_button_show_timetable(self):
        date = (self.mainWin.dateEdit_2.date()).toPyDate()
        self.mainWin.set_table_view()
        data = self.connect_DB.find_groups()
        for i in data:
            self.builder.set_groups(self.mainWin.tableWidget_2, i[0])
            item = self.connect_DB.find_timetable(date, i[0])
            for a in item:
                self.builder.set_line_table(self.mainWin.tableWidget_2, a)

    def push_button_export(self):
        if self.mainWin.tableWidget_2.horizontalHeaderItem(0):
            file = self.mainWin.set_file_name()
            if file:
                self.mainWin.create_workbook(file)
        else:
            self.mainWin.message_warning_empty_table()

    def push_button_edit(self):
        self.mainWin.tableWidget.setRowCount(0)
        date = self.mainWin.dateEdit_2.date().toPyDate()
        self.mainWin.dateEdit.setDate(date)
        data = self.connect_DB.find_groups()
        for i in data:
            self.builder.set_groups(self.mainWin.tableWidget, i[0])
            item = self.connect_DB.find_timetable(date, i[0])
            row = self.mainWin.tableWidget.rowCount()
            if not item:
                self.builder.set_button(self.mainWin.tableWidget)
            for a in item:
                self.mainWin.tableWidget.insertRow(row)
                self.builder.set_line_edit(self.mainWin.tableWidget, row, (a[2], a[3]))
                self.builder.set_button(self.mainWin.tableWidget, row)
                combo_lecturer, combo_subject, combo_classroom = self.builder.set_combo_box(self.mainWin.tableWidget,
                                                                                            row)
                row += 1
                self.set_combobox(combo_lecturer, combo_subject, combo_classroom)
                index = combo_lecturer.findText(a[0])
                combo_lecturer.setCurrentIndex(index)
                index = combo_subject.findText(a[1])
                combo_subject.setCurrentIndex(index)
                index = combo_classroom.findText(str(a[4]))
                combo_classroom.setCurrentIndex(index)
                self.builder.set_button(self.mainWin.tableWidget)
        self.mainWin.tabWidget.setCurrentIndex(0)

    def find_ID(self, group, subject, lecturer, classroom):
        ID_group = self.connect_DB.find_ID_groups(group)
        ID_subject = self.connect_DB.find_ID_subject(subject)
        ID_lecturer = self.connect_DB.find_ID_lecturer(lecturer)
        ID_classroom = self.connect_DB.find_ID_classroom(classroom)
        return ID_group, ID_subject, ID_lecturer, ID_classroom

    def save_row(self, group, subject, lecturer, classroom, date, lesson_number, comment):
        self.connect_DB.insert_into_timetable(group, subject, lecturer, classroom, date, lesson_number, comment)

    def set_subject(self, flag_show, comboBox=None):
        subject = self.connect_DB.find_subject()
        str_list = list()
        for i in subject:
            if flag_show == 0:
                comboBox.addItem(i[0])
                str_list.append(str(i[0]))
            elif flag_show == 1:
                self.mainWin.table_subject.setColumnCount(2)
                self.mainWin.table_subject.setHorizontalHeaderLabels(["Предмет", ''])
                self.builder.show_table(self.mainWin.table_subject, i[0])
        if comboBox:
            self.builder.search(str_list, comboBox)

    def set_classroom(self, flag_show, comboBox=None):
        classroom = self.connect_DB.find_classroom()
        str_list = list()
        for i in classroom:
            if flag_show == 0:
                comboBox.addItem(str(i[0]))
                str_list.append(str(i[0]))
            elif flag_show == 1:
                self.mainWin.table_classroom.setColumnCount(2)
                self.mainWin.table_classroom.setHorizontalHeaderLabels(["Номер аудитории", ''])
                self.builder.show_table(self.mainWin.table_classroom, i[0])
        if comboBox:
            self.builder.search(str_list, comboBox)

    def set_groups(self, flag_show=None):
        groups = self.connect_DB.find_groups()
        if not groups:
            self.mainWin.pushButton.setEnabled(False)
            return groups
        for i in groups:
            self.mainWin.pushButton.setEnabled(True)
            if flag_show == 0:
                self.builder.set_groups(self.mainWin.tableWidget, i[0])
                self.builder.set_button(self.mainWin.tableWidget)
            elif flag_show == 1:
                self.mainWin.table_groups.setColumnCount(2)
                self.mainWin.table_groups.setHorizontalHeaderLabels(["Группа", ''])
                self.builder.show_table(self.mainWin.table_groups, i[0])
        return groups

    def set_lecturer(self, flag_show, comboBox=None):
        snp = self.connect_DB.find_lecturer()
        str_list = list()
        for i in snp:
            if flag_show == 0:
                str_list.append(str(i[0]))
                comboBox.addItem(str(i[0]))
            elif flag_show == 1:
                self.mainWin.table_lecturer.setColumnCount(2)
                self.mainWin.table_lecturer.setHorizontalHeaderLabels(["Фамилия И.О.", ''])
                self.builder.show_table(self.mainWin.table_lecturer, i[0])
        if comboBox:
            self.builder.search(str_list, comboBox)

    def set_users(self):
        users = self.connect_DB.find_user()
        self.mainWin.table_user.setRowCount(0)
        for i in users:
            self.builder.show_table(self.mainWin.table_user, i, 2)
        if self.account:
            self.mainWin.set_account(self.account[0][0])

    def push_button_login(self):
        login, password = self.authorization.check_empty()
        if not login or not password:
            return

        print("_____ВХОД_____")
        data = self.connect_DB.find_user(login)
        print("Пользователь:", data)
        if self.authorization.check_login(data, password):
            print("ВХОД: OK\n")
            self.account = data
            self.push_button_update_table()
            self.authorization.close()
            if self.status != 1:
                self.mainWin.settings_for_user()
            self.mainWin.show()
            return
        print("ВХОД: ERROR\n")

    def push_button_add_user(self):
        login, password = self.authorization.check_empty()

        if not login or not password:
            return
        if self.connect_DB.find_user(login):
            self.mainWin.message_error_add_user()
            return

        print("________ADD USERS_______")
        salt, key = self.authorization.hash_password(password)
        data = list()
        data.append(login)
        data.append(key)
        data.append(salt)
        data.append(self.status)
        print("login:", login, ",\t pass:", password, "{", key, "}", ",\t status:", self.status)
        self.connect_DB.insert_into_user(data)
        self.mainWin.table_user.setRowCount(0)
        self.account.clear()
        self.set_users()

    def exit(self):
        self.mainWin.close()
        self.mainWin.tabWidget.setCurrentIndex(0)
        self.mainWin.tabWidget_2.setCurrentIndex(0)
        self.authorization.show()
