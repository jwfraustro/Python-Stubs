from PyQt5.QtCore import QThread, pyqtSignal


class ExampleThread(QThread):
    finished_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def do_work(self):

        for i in range(5):
            self.status_signal.emit(str(i))

        self.finished_signal.emit('Done!')

        return

    def run(self):
        self.do_work()
