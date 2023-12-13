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
import traceback


def output_err(e):
    error_class = e.__class__.__name__  # 取得錯誤類型
    detail = e.args[0]  # 取得詳細內容
    cl, exc, tb = sys.exc_info()  # 取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
    fileName = lastCallStack[0]  # 取得發生的檔案名稱
    lineNum = lastCallStack[1]  # 取得發生的行號
    funcName = lastCallStack[2]  # 取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
        fileName, lineNum, funcName, error_class, detail)
    print(errMsg)
    return (errMsg)


class MainWindow_controller(QtWidgets.QMainWindow):
    user_data = 'None'
    tweet_id = None
    data = ''
    # user_name = ''
    last_url = ''
    user_name = ''
    download_path = ''
    previousLink = ''
    exe_path = ''
    cookie = ''
    agent = ''
    recorder = ['']
    speed = [
        "自動",]

    show_recorder = []
    state = 'YES'

    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.thread1 = None  # 初始化執行緒

    def setup_control(self):
        self.user_data = os.getenv('APPDATA')+r'\twitter_download/'
        if not os.path.exists(self.user_data):
            os.mkdir(self.user_data)
        self.ui.download_speed.addItems(self.speed)
        self.get_user_json()
        self.load_user_data()
        self.ui.use_data.currentIndexChanged.connect(self.load_user_data)
        self.ui.use_data.setCurrentIndex(0)
        self.get_exe_path()

    def get_exe_path(self):
        if getattr(sys, 'frozen', False):  # 判断是exe还是.py程序
            self.exe_path = os.path.dirname(sys.executable)  # exe程序路径
        elif __file__:
            self.exe_path = os.path.dirname(__file__)  # .py程序路径

    def the_first_use(self):
        if os.path.isfile(self.user_data+'data.json'):
            time = (datetime.date.today()-datetime.timedelta(days=1)
                    ).strftime("%Y_%m_%d.json")
            os.rename(self.user_data+'data.json', self.user_data+time)
            with open(self.user_data+"json_recorder.txt", 'a+') as f:
                f.write(self.user_data+time+'\n')

    def get_user_json(self):
        try:
            data_list = (glob.glob(os.path.join(self.user_data, "*.json")))
            with open(self.user_data+"json_recorder.txt", 'w') as file:
                for i in data_list:
                    path = i.rsplit('\\', 1)
                    file.write(path[0]+'/'+path[1]+'\n')
        except:
            pass
        try:
            with open(self.user_data+"json_recorder.txt", 'r') as file:
                lines = [line.rstrip() for line in file]
            lines = list(dict.fromkeys(lines))
            with open(self.user_data+"json_recorder.txt", 'w') as file:
                for i in lines:
                    file.write(i+'\n')
            self.recorder = lines[::-1]
            self.show_recorder = [i.split('/')[1] for i in self.recorder]
            # print(self.recorder)
            self.ui.use_data.addItems(self.show_recorder)
        except:
            pass

    def save_info(self):
        jsonObject = {
            
            # "password":  self.ui.password.text(),
            "last_time_url": self.ui.last_url.text(),
            "previousLink": self.previousLink,
            "usr_path": self.ui.download_path.text(),
            "download_thread_num": self.ui.download_thread_num.value(),
            "exe_path": self.exe_path,
            "tweet_id": self.tweet_id,
            "cookie": self.ui.cookie.text(),
        }
        user_data = os.getenv('APPDATA')+r'\twitter_download/'
        fileName = user_data+datetime.date.today().strftime("%Y_%m_%d.json")

        with open(user_data+"json_recorder.txt", 'a+') as f:
            f.write(fileName+'\n')
        file = open(fileName, "w")
        json.dump(jsonObject, file, indent=4)
        file.close()

    def load_user_data(self):
        try:
            try:
                if (self.ui.use_data.currentIndex() == -1):
                    pre = 0
                else:
                    pre = self.ui.use_data.currentIndex()
            except:
                pre = 0
            # print(pre)
            # print(self.recorder[pre])
            if os.path.isfile(self.recorder[pre]):
                with open(self.recorder[pre]) as f:
                    data = json.load(f)
                print(data['email'])
                
                self.last_url = data['last_time_url']
                self.password = data['password']
                self.download_path = data['usr_path']
                self.exe_path = data['exe_path']
                self.download_thread_num = int(data['download_thread_num'])
                self.previousLink = data['previousLink']
                try:
                    self.tweet_id = data['tweet_id']
                    print(self.tweet_id)
                except Exception as err:
                    print(err)
                    self.tweet_id = None
                try:
                    self.cookie = data['cookie']
                    self.agent = data['agent']
                except:
                    pass
            else:
                print('no find')
            self.ui.address.setText(self.address)
            self.ui.password.setText(self.password)
            self.ui.last_url.setText(self.last_url)
            self.ui.user_name.setText(self.user_name)
            self.ui.download_path.setText(self.download_path)
            self.ui.cookie.setText(self.cookie)
            # self.ui.download_speed.setCurrentText(download_speed)
            self.ui.download_thread_num.setValue(self.download_thread_num)
        except Exception as e:
            output_err(e)
            pass

    @QtCore.pyqtSlot()
    def on_change_path_clicked(self):
        folder_path = QFileDialog.getExistingDirectory(None,
                                                       "Open folder",
                                                       "./")                 # start path
        # print(folder_path)
        self.ui.download_path.setText(folder_path)

    @QtCore.pyqtSlot()
    def on_start_clicked(self):
        self.ui.progressBar.setRange(0, 0)       # 兩個數值設定相同
        self.ui.progressBar.setValue(50)
        self.set_disabled()
        self.save_info()
        if self.state == 'NO':
            self.thread1 = twitter_get_url.download_thread(state='NO')
            self.thread1._progressbar.connect(self.progressbar_updata)
            self.thread1._finish.connect(self.thefinish)
            self.thread1._info_box.connect(self.show_info)
            self.thread1.start()
        else:

            self.thread1 = twitter_get_url.download_thread()
            self.thread1._progressbar.connect(self.progressbar_updata)
            self.thread1._finish.connect(self.thefinish)
            self.thread1._info_box.connect(self.show_info)
            self.thread1._err_box.connect(self.show_error_close)
            self.thread1.start()

    def update(self):
        user_data = os.getenv('APPDATA')+r'\twitter_download/'
        if not os.path.exists(user_data):
            os.mkdir(user_data)
        output = user_data+r'/check.json'
        # url='https://drive.google.com/u/1/uc?id=1uGppiPKA6TF0Zxz3SjCnAp_5_0YsPXYF&export=download'
        import requests
        url = 'https://drive.google.com/uc?id=1uGppiPKA6TF0Zxz3SjCnAp_5_0YsPXYF'
        response = requests.get(url, stream=True)
        with open(output, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        with open(output, encoding="utf-8") as file:  # 讀取寫入的文檔
            data = json.load(file)
        try:
            os.remove(output)
        except:
            pass
            # print("Could not remove")
        new_version = float(data['version'])
        version_info = data['update_info']
        version_state = data['activate'].upper()
        # print(version_state)
        if (version_state == 'NO'):
            self.state = version_state
            print('no')
            return
        # print(str(version_info))
        if (new_version > 2.0):
            # import requests

            response = requests.get("https://api.github.com/repos/[用户名]/[仓库名]/releases/latest")
            print(response.json()["tag_name"])

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

    def thefinish(self, state):
        if state == 1:
            QMessageBox.information(self, '完成', '下載成功')
            self.set_enable()
        elif state == -1:
            QMessageBox.information(self, '錯誤', '沒有需要下載的圖片')
            self.set_enable()
            self.ui.progressBar.setRange(0, 1)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)
        self.ui.progressBar.setRange(0, 1)
        self.set_enable()

    def show_error_close(self, title, message, second):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        # 設置關閉定時器
        timer = QTimer(msgBox)
        timer.setSingleShot(True)
        timer.timeout.connect(msgBox.close)
        timer.start(second)  # 5000 毫秒 = 5 秒
        # 顯示提示框
        msgBox.exec_()

    @QtCore.pyqtSlot()
    def on_clear_url_clicked(self):
        self.previousLink = 0

    def set_enable(self):
        self.ui.download_speed.setEnabled(True)
        self.ui.password.setEnabled(True)
        self.ui.last_url.setEnabled(True)
        self.ui.address.setEnabled(True)
        self.ui.user_name.setEnabled(True)
        self.ui.download_path.setEnabled(True)
        self.ui.change_path.setEnabled(True)
        self.ui.clear_url.setEnabled(True)
        self.ui.download_thread_num.setEnabled(True)
        self.ui.start.setEnabled(True)

    def set_disabled(self):
        self.ui.download_speed.setDisabled(True)
        self.ui.password.setDisabled(True)
        self.ui.last_url.setDisabled(True)
        self.ui.address.setDisabled(True)
        self.ui.user_name.setDisabled(True)
        self.ui.download_path.setDisabled(True)
        self.ui.change_path.setDisabled(True)
        self.ui.clear_url.setDisabled(True)
        self.ui.download_thread_num.setDisabled(True)
        self.ui.start.setDisabled(True)
