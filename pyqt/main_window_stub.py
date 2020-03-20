import main_window
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)


def main():
    win = QApplication([])
    win.setStyle("fusion")
    form = MainWindow()
    form.show()
    win.setActiveWindow(form)
    win.exec_()
