import sys

from PyQt5.QtWidgets import QApplication
import sources.Controller as Controller
import sources.TimeTable as TimeTable
import sources.Builder as Builder


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    controller = Controller.Controller()
    Builder.Builder(controller)  # Убрать 40 стр
    timetable = TimeTable.TimeTable(controller)
    timetable.show()
    app.exec()


if __name__ == '__main__':
    main()

