from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
import re
import os
import requests
import zipfile
import itertools,sys
from tkinter import *    #注意模塊導入方式，否則代碼會有差別，另見：import tkinter.messagebox 方法
from tkinter import messagebox
def getChromeDriver(options=None):
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.close()
        return
    except SessionNotCreatedException as e:

        driver_version = re.search(
            "Chrome version ([\d.]+)", str(e)).group(1)
        chrome_version = re.search(
            "Current browser version is ([\d.]+) with", str(e)).group(1)
        root = Tk()
        root.withdraw() 		 #****實現主窗口隱藏
        #root.update()  		 #*********需要update一下，不update也可以？
        messagebox.showinfo("提示：","驅動版本：%s\ngoogle瀏覽器版本：%s\n無法兼容\n開始更新驅動..."%(driver_version,chrome_version))    
        print(f"驅動版本：{driver_version}，google瀏覽器版本：{chrome_version}，不兼容\n開始更新驅動...")
        res = requests.get(
            "https://registry.npmmirror.com/-/binary/chromedriver/")
        versions = [obj["name"][:-1] for obj in res.json() if re.match("\d+",
                                                                       obj["name"]) and obj["name"].count(".") == 3]
        versions = {key: max(versions_split, key=lambda x: int(x[x.rfind(".")+1:]))
                    for key, versions_split in itertools.groupby(versions, key=lambda x: x[:x.rfind(".")])}
        dest_version = versions[chrome_version[:chrome_version.rfind(".")]]
        print("驅動將更新到", dest_version)
        if getattr(sys, 'frozen', False):  # 判断是exe还是.py程序
            exe_path = os.path.dirname(sys.executable)+'/'  # exe程序路径
        elif __file__:
            exe_path = os.path.dirname(__file__)+'/'  # .py程序路径  
        file = exe_path+f"chromedriver_{dest_version}_win32.zip"
        if not os.path.exists(file):
            url = f"https://registry.npmmirror.com/-/binary/chromedriver/{dest_version}/chromedriver_win32.zip"
            print("驅動下載地址：", url)
            res = requests.get(url)
            with open(file, 'wb') as f:
                f.write(res.content)
        else:
            print(file, "文件已經下載到當前目錄，下面直接使用緩存解壓覆蓋...")
        with zipfile.ZipFile(file) as zf:
            zf.extract("chromedriver.exe", ".")
        #driver = webdriver.Chrome(options=options)
        #return driver
        return

def update():
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging', 'enable-automation'])
    getChromeDriver(options)
