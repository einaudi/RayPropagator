import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtCore import Qt

from Widgets.MainWidget import MainWidget


class SliderPlot(QMainWindow):

    def __init__(self):

        super().__init__()

        self.main = MainWidget()

        self.setCentralWidget(self.main)
        self.setAttribute(Qt.WA_AlwaysShowToolTips, True)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SliderPlot()
    sys.exit(app.exec_())