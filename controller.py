import os
import json
from PyQt5 import QtWidgets, QtCore
from ui_twitterdownload import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import glob
import twitter_get_url
import sys
import datetime
from PyQt5.QtCore import QTimer
from tools import output_err
from write_and_read_json import user_data


class MainWindow_controller(QtWidgets.QMainWindow):
    tweet_id = None
    data = ''
    exe_path = ''
    recorder = ['']
    show_recorder = []

    def __init__(self):
        super().__init__()  # 調用父類的構造函數
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.thread1 = None  # 初始化執行緒
        self.usr_data = user_data()

    def setup_control(self):
        # pass
        if not self.usr_data.read_info():
            self.show_info('錯誤', '讀取設定檔失敗，請重新設定')
        else:
            self.put_info()
            self.ui.use_data.addItems(self.usr_data.show_recorder)
        self.ui.use_data.currentIndexChanged.connect(self.changeinfo)
        self.ui.use_data.setCurrentIndex(0)
        # self.get_exe_path()

    def changeinfo(self):
        self.usr_data.read_info(self.ui.use_data.currentIndex())
        self.put_info()

    def update_info(self):
        self.usr_data.download_path = self.ui.download_path.text()
        self.usr_data.download_thread_num = self.ui.download_thread_num.value()
        self.usr_data.cookie = self.ui.cookie.text()
        # self.usr_data.auto_update = self.ui.auto_update.isChecked()
        self.usr_data.last_time_url = self.ui.last_url.text()
        self.usr_data.usr_name = self.ui.user_name.text()

    def put_info(self):
        self.ui.download_path.setText(self.usr_data.download_path)
        self.ui.download_thread_num.setValue(self.usr_data.download_thread_num)
        self.ui.cookie.setText(self.usr_data.cookie)
        # self.ui.auto_update.setChecked(self.auto_update)
        self.ui.user_name.setText(self.usr_data.usr_name)
        self.ui.last_url.setText(self.usr_data.last_time_url)

    @QtCore.pyqtSlot()
    def on_change_path_clicked(self):
        folder_path = QFileDialog.getExistingDirectory(None,
                                                       "Open folder",
                                                       "./")                 # start path
        # print(folder_path)
        self.ui.download_path.setText(folder_path)
        self.usr_data.download_path = folder_path

    @QtCore.pyqtSlot()
    def on_start_clicked(self):
        self.update_info()
        self.usr_data.save_info()
        self.set_ui_enabled(False)
        # while (1):
        #     pass
    #     self.ui.progressBar.setRange(0, 0)       # 兩個數值設定相同
    #     self.ui.progressBar.setValue(50)
#         self.thread1 = twitter_get_url.download_thread()
#         self.thread1._progressbar.connect(self.progressbar_updata)
#         self.thread1._finish.connect(self.thefinish)
#         self.thread1._info_box.connect(self.show_info)
#         self.thread1._err_box.connect(self.show_error_close)
#         self.thread1.start()

    def progressbar_updata(self, step, max):
        if (step == 1):
            self.ui.progressBar.setRange(1, max+1)
            self.ui.progressBar.setValue(self.ui.progressBar.value()+step)
            self.ui.progressBar.setFormat("正在下載...%v/%m")
        elif (step == 2):
            self.ui.progressBar.setRange(0, 1)
            self.ui.progressBar.setValue(0)
        elif (step == -1):
            self.ui.progressBar.setRange(0, max-1)       # 兩個數值設定相同
            self.ui.progressBar.setValue(0)
            self.ui.progressBar.setFormat("正在抓取喜歡的貼文..."+str(max-1))

    # def thefinish(self, state):
    #     if state == 1:
    #         QMessageBox.information(self, '完成', '下載成功')
    #         self.set_enable()
    #     elif state == -1:
    #         QMessageBox.information(self, '錯誤', '沒有需要下載的圖片')
    #         self.set_enable()
    #         self.ui.progressBar.setRange(0, 1)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)
        self.ui.progressBar.setRange(0, 1)

    # def show_error_close(self, title, message, second):
    #     msgBox = QMessageBox()
    #     msgBox.setText(message)
    #     msgBox.setWindowTitle(title)
    #     # 設置關閉定時器
    #     timer = QTimer(msgBox)
    #     timer.setSingleShot(True)
    #     timer.timeout.connect(msgBox.close)
    #     timer.start(second)  # 5000 毫秒 = 5 秒
    #     # 顯示提示框
    #     msgBox.exec_()

    @QtCore.pyqtSlot()
    def on_clear_url_clicked(self):
        self.usr_data.previousLink = 0

    def set_ui_enabled(self, enabled):
        self.ui.last_url.setEnabled(enabled)
        self.ui.user_name.setEnabled(enabled)
        self.ui.download_path.setEnabled(enabled)
        self.ui.change_path.setEnabled(enabled)
        self.ui.clear_url.setEnabled(enabled)
        self.ui.download_thread_num.setEnabled(enabled)
        self.ui.start.setEnabled(enabled)
