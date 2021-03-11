import sys

from PyQt5.QtWidgets import QApplication

import sources.Authorization as Authorization
import sources.Builder as Builder
import sources.Controller as Controller
import sources.TimeTable as TimeTable


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    controller = Controller.Controller()
    Builder.Builder(controller)
    TimeTable.TimeTable(controller)
    authorization = Authorization.Authorization(controller)
    authorization.show()
    app.exec()


if __name__ == '__main__':
    main()
