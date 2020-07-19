import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from UI import Example, Stream

class MainWindow(QMainWindow, Example):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        #sys.stdout = Stream(newText=self.outputWritten)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywin = MainWindow()
    mywin.show()
    sys.exit(app.exec_())