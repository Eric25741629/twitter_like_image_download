# tools.py
import sys
import traceback
import os


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


def get_exe_path():
    if getattr(sys, 'frozen', False):  # 判断是exe还是.py程序
        return os.path.dirname(sys.executable)  # exe程序路径
    elif __file__:
        return os.path.dirname(__file__)  # .py程序路径

    # def update(self):
    #     self.user_data = os.path.join(os.getenv('APPDATA'), 'twitter_download')
    #     if not os.path.exists(self.user_data):
    #         os.mkdir(self.user_data)
    #     output = self.user_data+r'/check.json'
    #     # url='https://drive.google.com/u/1/uc?id=1uGppiPKA6TF0Zxz3SjCnAp_5_0YsPXYF&export=download'
    #     import requests
    #     url = 'https://drive.google.com/uc?id=1uGppiPKA6TF0Zxz3SjCnAp_5_0YsPXYF'
    #     response = requests.get(url, stream=True)
    #     with open(output, 'wb') as f:
    #         for chunk in response.iter_content(chunk_size=1024):
    #             if chunk:
    #                 f.write(chunk)
    #     with open(output, encoding="utf-8") as file:  # 讀取寫入的文檔
    #         data = json.load(file)
    #     try:
    #         os.remove(output)
    #     except:
    #         pass
    #         # print("Could not remove")
    #     new_version = float(data['version'])
    #     version_info = data['update_info']
    #     version_state = data['activate'].upper()
    #     # print(version_state)
    #     if (version_state == 'NO'):
    #         self.state = version_state
    #         print('no')
    #         return
    #     # print(str(version_info))
    #     if (new_version > 2.0):
    #         # import requests

    #         response = requests.get(
    #             "https://api.github.com/repos/[用户名]/[仓库名]/releases/latest")
    #         print(response.json()["tag_name"])
