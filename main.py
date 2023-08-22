from PyQt5 import QtWidgets
from controller import MainWindow_controller
from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QMessageBox
from time import sleep
import sys
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    try:
        window.update()
    except:
        QMessageBox.information(None, '通知', '獲取更新失敗')
    #sleep(3)
    window.show()
    window.setup_control()
    sys.exit(app.exec_())
    