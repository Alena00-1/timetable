from PyQt5.QtCore import Qt, QObject, QStringListModel
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QComboBox, QLineEdit, QCompleter


class Builder(QObject):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.set_builder(self)

    @staticmethod
    def set_groups(table, data):
        table.setRowCount(table.rowCount() + 1)
        table.setSpan(table.rowCount() - 1, 0, 1, 2)
        item = QTableWidgetItem(str(data))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(QColor(240, 240, 240)))
        table.setItem(table.rowCount() - 1, 0, item)
        for column in range(2, 6):
            empty_item = QTableWidgetItem()
            empty_item.setBackground(QBrush(QColor(240, 240, 240)))
            table.setItem(table.rowCount() - 1, column, empty_item)

    def set_button(self, table, row=None):
        if row:
            but = QPushButton(table)
            but.setText("Удалить")
            table.setCellWidget(row, 5, but)
            but.clicked.connect(lambda: self.controller.push_button_remove_row(0))
        else:
            table.setRowCount(table.rowCount() + 1)
            table.setSpan(table.rowCount() - 1, 0, 1, 6)
            but = QPushButton(table)
            but.setText("Добавить...")
            table.setCellWidget(table.rowCount() - 1, 0, but)
            but.clicked.connect(self.controller.push_button_add_row)

    @staticmethod
    def set_line_edit(table, row, data=None):
        if not data:
            for i in range(2, 4):
                table.setCellWidget(row, i, QLineEdit())
        else:
            item_1 = QLineEdit()
            item_2 = QLineEdit()
            item_1.setText(str(data[0]))
            item_2.setText(str(data[1]))
            table.setCellWidget(row, 2, item_1)
            table.setCellWidget(row, 3, item_2)

    @staticmethod
    def set_combo_box(table, row):
        combo_lecturer = QComboBox(table)
        combo_subject = QComboBox(table)
        combo_classroom = QComboBox(table)
        combo_lecturer.setEditable(True)
        combo_subject.setEditable(True)
        combo_classroom.setEditable(True)

        table.setCellWidget(row, 0, combo_lecturer)
        table.setCellWidget(row, 1, combo_subject)
        table.setCellWidget(row, 4, combo_classroom)
        return combo_lecturer, combo_subject, combo_classroom

    def show_table(self, table, data, column=1):
        table.setRowCount(table.rowCount() + 1)
        but = QPushButton(table)
        but.setText("Удалить")
        table.setCellWidget(table.rowCount() - 1, column, but)
        but.clicked.connect(lambda: self.controller.push_button_delete(table))
        if isinstance(data, tuple):
            table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(str(data[0])))
            table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(str(data[1])))
        else:
            table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(str(data)))

    @staticmethod
    def remove_row(table, count):
        row = table.currentIndex().row()
        table.removeRow(row - count)

    @staticmethod
    def set_line_table(table, data):
        table.setRowCount(table.rowCount() + 1)
        for i in range(5):
            item = QTableWidgetItem(str(data[i]))
            table.setItem(table.rowCount() - 1, i, item)

    def search(self, str_list, widget):
        model = QStringListModel()
        model.setStringList(str_list)
        completer = QCompleter()
        completer.setModel(model)
        widget.setCompleter(completer)
