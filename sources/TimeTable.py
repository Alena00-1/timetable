import datetime

import xlsxwriter
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QMessageBox, QComboBox, QPushButton, QLineEdit, QFileDialog

import resourses.mainWin as mainWin


class TimeTable(QMainWindow, mainWin.Ui_MainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller
        self.controller.set_timeTable(self)
        self.setup_settings()

    def setup_settings(self):
        self.setWindowIcon(QIcon('book.png'))
        self.tabWidget.setCurrentIndex(0)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.progressBar.setVisible(False)
        self.progressBar_2.setVisible(False)
        self.export_button.setVisible(False)
        self.edit_button.setVisible(False)

        self.tableWidget.setColumnCount(6)
        self.table_lecturer.setColumnCount(2)
        self.table_groups.setColumnCount(2)
        self.table_subject.setColumnCount(2)
        self.table_classroom.setColumnCount(2)

        self.tableWidget.setHorizontalHeaderLabels(
            ["Преподаватель", "Предмет", 'Пара', 'Примечание', "Аудитория", 'Редактировать'])
        self.table_lecturer.setHorizontalHeaderLabels(["Фамилия И.О.", ''])
        self.table_classroom.setHorizontalHeaderLabels(["Номер аудитории", ''])
        self.table_subject.setHorizontalHeaderLabels(["Предмет", ''])
        self.table_groups.setHorizontalHeaderLabels(["Группа", ''])

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_lecturer.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_groups.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_subject.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_classroom.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.button_subject.clicked.connect(self.controller.push_button_add_subject)
        self.button_classroom.clicked.connect(self.controller.push_button_add_classroom)
        self.button_group.clicked.connect(self.controller.push_button_add_group)
        self.button_lecturer.clicked.connect(self.controller.push_button_add_lecturer)
        self.pushButton.clicked.connect(self.controller.push_button_save)
        self.update_button.clicked.connect(self.controller.push_button_update_table)
        self.pushButton_2.clicked.connect(self.controller.push_button_show_timetable)
        self.export_button.clicked.connect(self.controller.push_button_export)
        self.edit_button.clicked.connect(self.controller.push_button_edit)

        self.controller.push_button_update_table()
        self.dateEdit_2.setDate(datetime.datetime.now())
        self.dateEdit.setDate(datetime.datetime.now())
        self.edit_classroom.setValidator(QIntValidator())

    def message_error_lecturer(self):
        QMessageBox.critical(self, 'Внимание!', "Нет доступных преподавателей!")

    def message_error_classroom(self):
        QMessageBox.critical(self, 'Внимание!', "Нет доступных аудиторий!")

    def message_error_subject(self):
        QMessageBox.critical(self, 'Внимание!', "Нет доступных предметов!")

    def message_warning_empty_group(self):
        QMessageBox.warning(self, 'Предупреждение', "В базе нет ни одной группы")

    def message_warning_empty_value(self):
        QMessageBox.warning(self, 'Сохранение не выполнено',
                            "Необходимо проверить и исправить поля отмеченные красным цветом.\n"
                            "*Если выделено поле 'Преподаватель' - данный преподаватель уже занят на выбранный номер пары.\n"
                            "*Если выделено поле 'Аудитория' - данная аудитория уже занята на выбранный номер пары.\n"
                            "*Если выделено поле 'Пара' - его необходимо заполнить.")

    def message_warning_empty_table(self):
        QMessageBox.warning(self, 'Предупреждение', "Нет данных для экспорта.")

    def message_success_save(self):
        QMessageBox.about(self, 'Сохранение выполнено', "Расписание успешно сохранено.")

    def message_error_save(self):
        QMessageBox.critical(self, 'Ошибка!', "Не удалось сохранить в файл.")

    def create_table(self):
        check = self.check_empty_value(self.tableWidget.rowCount())
        if not check:
            return
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(self.tableWidget.rowCount() - 2)
        self.tableWidget.setEnabled(False)
        self.group_ = self.tableWidget.item(0, 0).text()
        for i in range(1, self.tableWidget.rowCount() - 1):
            widget = self.tableWidget.cellWidget(i, 0)
            if isinstance(widget, QComboBox):
                lecturer = widget.currentText()
                widget = self.tableWidget.cellWidget(i, 1)
                subject = widget.currentText()
                widget = self.tableWidget.cellWidget(i, 2)
                lesson_number = widget.text().strip()
                widget = self.tableWidget.cellWidget(i, 3)
                comment = widget.text().strip()
                widget = self.tableWidget.cellWidget(i, 4)
                classroom = widget.currentText()
                group, subject, lecturer, classroom = self.controller.find_ID(self.group_, subject, lecturer,
                                                                              classroom)
                date = (self.dateEdit.date()).toPyDate()
                self.controller.save_row(group, subject, lecturer, classroom, date,
                                         lesson_number, comment)
                self.progressBar.setValue(i)
            elif isinstance(widget, QPushButton):
                self.group_ = self.tableWidget.item(i + 1, 0).text()
                self.progressBar.setValue(i)
            else:
                self.progressBar.setValue(i)
        self.tableWidget.setEnabled(True)
        self.message_success_save()
        self.controller.push_button_update_table()
        self.progressBar.setVisible(False)

    def empty_value(self, widget):
        if isinstance(widget, QLineEdit):
            widget.setStyleSheet("QLineEdit { border: 1px solid red;}")
        elif isinstance(widget, QComboBox):
            widget.setStyleSheet("QComboBox { border: 1px solid red;}")

    def clear_mask(self, widget=None):
        if not widget:
            edit = [self.edit_lecturer, self.edit_classroom, self.edit_subject, self.edit_group]
            for i in edit:
                i.setStyleSheet('border: 1px solid gray; border-radius: 4px;')
            return
        widget.setStyleSheet('')

    def check_empty_value(self, row):
        self.timetable = dict()
        self.classroom = dict()
        self.save = True
        for i in range(1, row):
            combobox_lecturer = self.tableWidget.cellWidget(i, 0)
            if not isinstance(combobox_lecturer, QComboBox):
                continue
            line_edit = self.tableWidget.cellWidget(i, 2)
            lesson_number = line_edit.text().strip()
            combobox_classroom = self.tableWidget.cellWidget(i, 4)
            self.clear_mask(line_edit)
            self.clear_mask(combobox_lecturer)
            self.clear_mask(combobox_classroom)
            if not lesson_number:
                self.save = False
                self.empty_value(line_edit)
            else:
                self.check_lecturer(combobox_lecturer, lesson_number)
                self.check_classroom(combobox_classroom, lesson_number)
        if not self.save:
            self.message_warning_empty_value()
            return False
        return True

    def check_lecturer(self, combobox_lecturer, lesson_number):
        lecturer = combobox_lecturer.currentText()
        if lecturer not in self.timetable:
            self.timetable[lecturer] = [lesson_number]
            return
        if lesson_number in self.timetable.get(lecturer):
            self.save = False
            self.empty_value(combobox_lecturer)
        else:
            self.timetable.update({lecturer: [lesson_number]})

    def check_classroom(self, combobox_classroom, lesson_number):
        classroom_number = combobox_classroom.currentText()
        if classroom_number not in self.classroom:
            self.classroom[classroom_number] = [lesson_number]
            return
        if lesson_number in self.classroom.get(classroom_number):
            self.save = False
            self.empty_value(combobox_classroom)
        else:
            self.classroom.update({classroom_number: [lesson_number]})

    def set_table_view(self):
        self.export_button.setVisible(True)
        self.edit_button.setVisible(True)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget_2.setHorizontalHeaderLabels(
            ["Преподаватель", "Предмет", 'Пара', 'Примечание', "Аудитория"])
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def create_workbook(self, file):
        self.tableWidget_2.setDisabled(True)
        self.progressBar_2.setVisible(True)
        self.progressBar_2.setMaximum(self.tableWidget_2.rowCount() * self.tableWidget_2.columnCount())
        workbook = xlsxwriter.Workbook(file)
        worksheet = workbook.add_worksheet(str(self.dateEdit_2.date().toPyDate()))
        date = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center'})
        header_format = workbook.add_format({
            'border': 1,
            'bg_color': '#608CBB',
            'color': 'white',
            'bold': True,
            'align': 'center',
        })
        group_format = workbook.add_format({
            'border': 1,
            'bg_color': '#608CBB',
            'color': 'white',
            'bold': True,
            'align': 'center',
        })
        worksheet.merge_range('A1:E1', self.dateEdit_2.date().toPyDate(), date)
        for i in range(5):
            worksheet.write(1, i, self.tableWidget_2.horizontalHeaderItem(i).text(), header_format)
        for row in range(self.tableWidget_2.rowCount()):
            for column in range(self.tableWidget_2.columnCount()):
                try:
                    worksheet.write(row + 2, column, self.tableWidget_2.item(row, column).text())
                    self.group = self.tableWidget_2.item(row, column).text()
                except AttributeError:
                    if column == 1:
                        worksheet.merge_range(row + 2, column - 1, row + 2, 1, self.group, group_format)
                        for i in range(1, 4):
                            worksheet.write_blank(row + 2, column + i, '', group_format)
                finally:
                    self.progressBar_2.setValue(self.progressBar_2.value() + 1)
        try:
            workbook.close()
            self.message_success_save()
        except Exception:
            self.message_error_save()
        finally:
            self.progressBar_2.setVisible(False)
            self.tableWidget_2.setEnabled(True)

    def set_file_name(self):
        date = (self.dateEdit_2.date()).toPyDate()
        f = QFileDialog.getSaveFileName(self, 'Сохранить расписание', f'timetable({date})', '.xlsx(*.xlsx)')
        if f == ('', ''):
            return
        else:
            return f[0]
