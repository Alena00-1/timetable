import sys

from PyQt5.QtWidgets import QApplication

import sources.Builder as Builder
import sources.Controller as Controller
import sources.TimeTable as TimeTable


def main():
    controller = Controller.Controller()
    Builder.Builder(controller)
    timetable = TimeTable.TimeTable(controller)
    timetable.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main()
    app.exec()
