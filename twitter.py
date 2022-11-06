from sre_parse import State
import tkinter as tk
from turtle import bgcolor
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tama,aqua,aqua2
import os,base64
from PIL import Image, ImageTk
from tkinter import Tk, BOTH, Menu
from tkinter import filedialog
import tkinter.messagebox
from time import sleep
import random
from requests import exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import win32api
import threading
import gdown
import sys
from bs4 import BeautifulSoup
import requests
import datetime
import thesamedel
from selenium.common.exceptions import SessionNotCreatedException

import urllib3,json,re
import update_selenium
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)        
option = webdriver.ChromeOptions()
import zipfile
option.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
global window2_state

window2_state=0
def logging(driver,address,password,user_name):
    url = 'https://twitter.com/i/flow/login'
    #driver = webdriver.Chrome(options=option)
    driver.get(url)
    sleep(5)
    driver.find_element(By.TAG_NAME,'input').send_keys(address)
    sleep(5)
    buttons = driver.find_elements(By.CSS_SELECTOR,'div[role="button"]')
    for i in buttons:
        if i.text == '下一步' or i.text == 'Next':
            i.click()   # 如果按鈕是「下一步」或「Next」就點擊
            break
    sleep(5)     # 等待兩秒頁面載入後繼續
    try:
        check = driver.find_element(By.CSS_SELECTOR,'input[autocomplete="on"]')
        check.send_keys(user_name)    # 輸入帳號
        buttons = driver.find_elements(By.CSS_SELECTOR,'div[role="button"]')
        for i in buttons:
            if i.text == '下一步' or i.text == 'Next':
                i.click()  # 如果按鈕是「下一步」或「Next」就點擊
                print('驗證使用者帳號，點擊下一步')
                break
            sleep(2)       # 等待兩秒頁面載入後繼續
    except:
        print('ok')
    sleep(2+random.random())    
    pwd = driver.find_element(By.CSS_SELECTOR,'input[autocomplete="current-password"]')
    pwd.send_keys(password)
    print('輸入密碼')
    buttons = driver.find_elements(By.CSS_SELECTOR,'div[role="button"]')
    for i in buttons:
        if i.text == '登入' or i.text == 'Log in':
            i.click()
            print('點擊登入')
            break
    sleep(5+random.random())
def download_link(res,exist_link,download,lastlink):
    for image in res:
        if exist_link in image['src']:
            return -1
        elif lastlink in image['src']:
            return -2
        elif image['alt']=='圖片':
            print(image['src'])
            if image['src'] not in download:
                download.add(image['src'])
    global know_num
    know_num=len(download)
    return 0
def download_twitter_img(filepath,link):
    try:
        for i in range(0,3):
            name=link.replace("https://pbs.twimg.com/media/","").split("?")[0]
            url=link.replace("?format=",".").rsplit("&")[0]+":orig"
            headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
                        }
            print(url)
            htmlfile = requests.get(url,headers=headers,verify=False,stream=True,timeout=5)
            htmlfile.raise_for_status() 
            size = 0
            chunk_size = 1024
            if ".jpg"in url:
                name=name+".jpg"
            elif ".png"in url:
                name=name+".png"
            try:
                with open(filepath+name,'wb') as file: #显示进度条
                        for data in htmlfile.iter_content(chunk_size = chunk_size):
                            file.write(data)
                            size +=len(data)  
            except:
                try:
                    with open(filepath+'1'+name,'wb') as file: #显示进度条
                            for data in htmlfile.iter_content(chunk_size = chunk_size):
                                file.write(data)
                                size +=len(data) 
                except Exception as err:
                    print(err)
            break
    except Exception as err:
            print(err)
    return 
def newfile():
    tkinter.messagebox.showinfo("開新檔案","可在此撰寫開新檔案程式碼")
#D:\python\envs\photo\Lib\site-packages\selenium\webdriver\common\service.py有修改過  from win32process import CREATE_NO_WINDOW 
'''self.process= subprocess.Popen(cmd, env=self.env,
close_fds=platform.system() != 'Windows',
stdout=self.log_file, stderr=self.log_file,
stdin=PIPE, creationflags=CREATE_NO_WINDOW)
'''  
#168
def savefile():
    comboExample = ttk.Combobox(window1, 
                            values=[
                                    "January", 
                                    "February",
                                    "March",
                                    "April"])
def about():
    tkinter.messagebox.showinfo("程式說明","作者:吳柏憲")

    tkinter.messagebox.showinfo("下次更新:","提高速度")
def writedata(address,password,link,user_name,download_path,lastlink='none',exe_path='none',version=0):
    jsonObject = {
    "username": usr_name.get(),
    "email": usr_address.get(),
    "password": usr_password.get(),
    "last_time_url": link, 
    "last_last_time_url": lastlink,
    "usr_path": usr_path.get(),
    "download_speed": download_speed.get(),
    "download_thread_num": download_thread_num.get(),
    "exe_path":exe_path
    }
    
    user_data=os.getenv('APPDATA')+r'\twiter_download/'
    fileName = user_data+"data.json"
    file = open(fileName, "w")
    json.dump(jsonObject, file, indent = 4)
    file.close()
    f = open((user_data+"password.txt"), "w+")
    f.write(address+"\n")
    f.write(password+"\n")
    f.write(link+"\n")
    f.write(user_name+"\n")
    f.write(download_path+"\n")
    f.write(lastlink+"\n")
    f.write(exe_path+"\n")
    f.write(str(0)+"\n")
    f.close()
    
def Userinfo():
    try:
        user_data=os.getenv('APPDATA')+r'\twiter_download/'
        if os.path.isfile(user_data+'data.json'):
            with open(user_data+'data.json') as f:
                data = json.load(f)
            address=data['email']
            user_name=data['username']
            link=data['last_time_url']
            password=data['password']
            download_path=data['usr_path']
            download_speed.set(data['download_speed'])
            download_thread_num.set(data['download_thread_num'])
        elif os.path.isfile(user_data+'password.txt'):
            with open((user_data+'password.txt')) as file:     #讀取寫入的文檔
                lines = [line.rstrip() for line in file]
            address=lines[0]
            password=lines[1]
            link=lines[2]
            user_name=lines[3]
            download_path=lines[4]
        var_usr_address.set(address)
        var_usr_password.set(password)
        var_usr_url.set(link)
        var_usr_name.set(user_name)
        var_usr_path.set(download_path)
    except:
        pass
    
def lockinput():
    b['state'] = tk.DISABLED
    downloadpath['state'] = tk.DISABLED
    usr_address.configure(state='disabled')
    usr_password.configure(state='disabled')
    url.configure(state='disabled')
    usr_name.configure(state='disabled')
    usr_path.configure(state='disabled')
def unlockinput():
    b['state'] = tk.NORMAL
    usr_address.configure(state='normal')
    usr_password.configure(state='normal')
    url.configure(state='normal')
    usr_name.configure(state='normal')
    usr_path.configure(state='normal')
    downloadpath['state'] = tk.NORMAL
def open_the_info_file():
    user_data=os.getenv('APPDATA')+r'\twiter_download/'
    os.system(user_data+'data.json')

    
def use_info_check():
    address=usr_address.get()
    password=usr_password.get()
    last_url=url.get()
    name=usr_name.get()
    path=usr_path.get()
    if address=="":
        tkinter.messagebox.showinfo(title='警告', message='帳號不得為空！') 
        return -1
    if password=="":
        tkinter.messagebox.showinfo(title='警告', message='密碼不得為空！') 
        return -1
    if name=="":
        tkinter.messagebox.showinfo(title='警告', message='名稱不得為空！') 
        return -1
    if last_url=="":
        ask=tkinter.messagebox.askquestion(title='沒有網址', message='是否繼續?')
        if ask=='yes':
            print('ok')
            last_url=0
            return 2
        else:
            return-1
    if path=="":
        tkinter.messagebox.showinfo(title='警告', message='路徑不得為空！') 
        return -1
def begin():
    lockinput()
    window2.after(10, update_bar)
    window1.withdraw()
    #window.destroy()
    sleep(1)
    window2.deiconify()
    threads=[]
    threads.append(threading.Thread(target =beginthin, args = ()))
    threads.append(threading.Thread(target =download_update, args = ()))
    threads[0].daemon = True 
    threads[0].start()
    threads[1].daemon = True 
    threads[1].start()
global download_num  
download_num=0

   # window.geometry("0x0")
def beginthin():
    
    address=usr_address.get()
    password=usr_password.get()
    last_url=url.get()
    name=usr_name.get()
    path=usr_path.get()
    test=use_info_check()
    speed=download_speed.get()
    th_num=download_thread_num.get()
    print(speed)
    if test==2:
        last_url=0
    if test==-1:
        unlockinput()
        return
    
    user_data=os.getenv('APPDATA')+r'\twiter_download/'
    
    if os.path.exists(user_data):
        if os.path.isfile(user_data+'data.json'):
            with open(user_data+'data.json') as f:
                data = json.load(f)
                lastlink=data['last_last_time_url']
        elif os.path.isfile(user_data+'password.txt'):
            with open((user_data+'password.txt')) as file:     #讀取寫入的文檔
                lines = [line.rstrip() for line in file]
                try:
                    lastlink=lines[5]
                except:
                    lastlink=""
    elif not os.path.exists(user_data):
        #print('mkdir ' + path)
        os.mkdir(user_data)
    if getattr(sys, 'frozen', False):  # 判断是exe还是.py程序
        exe_path = os.path.dirname(sys.executable)  # exe程序路径
    elif __file__:
        exe_path = os.path.dirname(__file__)  # .py程序路径    
    writedata(address,password,last_url,name,path,lastlink,exe_path)
    win32api.ShellExecute(0, 'open', 'chrome.exe', '--headless --disable-backgrounding-occluded-windows --topmost --remote-debugging-port=9527 --user-data-dir='+user_data+'/twitter_log ', '',0)
    try:
        driver = webdriver.Chrome(options=option)
    except Exception as e:    
        update_selenium.update()
        try:
            driver = webdriver.Chrome(options=option)
        except Exception as e: 
            tkinter.messagebox.showinfo(title='錯誤', message=e) 
            os._exit(0)
    sleep(3)
    driver.get('https://twitter.com/'+name+'/likes')
    sleep(3)
    driver.execute_script("document.body.style.transform='scale(0.2)'")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    res=(soup.find_all("span"))
    for rules in res:
        if "登入"in rules:
            print('尚未登入')
            logging(driver,address,password,name)
            driver.get('https://twitter.com/'+name+'/likes')   
    while(1):
        soup = BeautifulSoup(driver.page_source, 'lxml')
        res=soup.find_all("article")
        if(len(res)>=2):
            break   
    download=set()
     
    last_url_name=last_url.replace("https://pbs.twimg.com/media/","").split("?format=")[0]
    lastlink_name=lastlink.replace("https://pbs.twimg.com/media/","").split("?format=")[0]
    global check
    check=2
    for retrytime in range(0,3):
        while(1):
            soup = BeautifulSoup(driver.page_source, 'lxml')
            res=soup.find_all("img")
            #print(link)
            err=download_link(res,last_url_name,download,lastlink)
            if err==-1:
                break
            if err==-2:
                break
            try:
                js = 'var divA= document.querySelector("[data-testid=\'cellInnerDiv\']"); divA.remove(divA);'
                driver.execute_script(js)
            except:
                try:
                    if(speed=='自動'):
                        while(1):
                            soup = BeautifulSoup(driver.page_source, 'lxml')
                            res=soup.find_all("img")
                            if(len(res)>=5):
                                break
                    elif(speed=='快'):
                        sleep(0.5)
                    elif(speed=='普通'):
                        sleep(1)
                    elif(speed=='慢'):
                        sleep(2)
                    js = 'var divA= document.querySelector("[data-testid=\'cellInnerDiv\']"); divA.remove(divA);'
                    driver.execute_script(js)
                except Exception as err:
                    print(err)
                    print('滑到底部 出錯')
                    err=-2
            print("往下滑")
            if(speed=='自動'):
                while(1):
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    res=soup.find_all("article")
                    if(len(res)>=2):
                        break
            if(speed=='快'):
                sleep(0.5)
            elif(speed=='普通'):
                sleep(1)
            elif(speed=='慢'):
                sleep(2)
        if err==-1:
            break
        elif err==-2:
            driver.get('https://twitter.com/'+name+'/likes')
            driver.execute_script("document.body.style.transform='scale(0.7)'")
            sleep(4+random.random())
            download=set()
    driver.close()
    check=0
    if not os.path.exists(path):
        os.mkdir(path)
    download = list(download)
    if download!=[]:
        download_thread=[]
        global download_all_num
        download_all_num=len(download)
        for i in range(len(download)-1,-1,-1):
            download_thread.append(threading.Thread(target =download_twitter_img, args = (path+'/',download[i])))
        downloadtimes=0
        global download_num  
        for i in range(0,len(download)):
            print(i)
            #print(download[i])
            
            download_num=i
            download_thread[i].start()
            #download_twitter_img(path+'/',download[i])
            downloadtimes+=1
            while (threading.active_count())>int(th_num)+1:
                sleep(0.01)
            '''if (stop-start)<1:
                sleep(1-stop+start)'''
        for i in range(0,len(download)):
            download_thread[i].join()
        writedata(address,password,download[0],name,path,last_url,exe_path,'0')   
        tkinter.messagebox.showinfo(title='完成', message='下載成功') 
    else:
        tkinter.messagebox.showinfo(title='錯誤', message='沒有需要下載的圖片') 
    ask=0
    check=1
    #window1.deiconify()
    unlockinput()
global check
check=0
def path():
    root = tk.Tk()
    root.withdraw()
    download_path = filedialog.askdirectory()
    root.destroy()
    var_usr_path.set(download_path)
def download_update():
    user_data=os.getenv('APPDATA')+r'\twiter_download/'
    if os.path.exists(user_data):
        if not os.path.isfile(user_data+'updata.exe'):
            print('沒有更新器')
            url='https://drive.google.com/u/1/uc?id=10Jsyvr11wp9DT3oX9AbXdotwHYBZJqx8&export=download'
            exe=user_data+"updata.exe"
            gdown.download(url,exe)
def update(x=0):
    if getattr(sys, 'frozen', False):  # 判断是exe还是.py程序
        exe_path = os.path.dirname(sys.executable)  # exe程序路径
    elif __file__:
        exe_path = os.path.dirname(__file__)  # .py程序路径
    user_data=os.getenv('APPDATA')+r'\twiter_download/'
    output=user_data+r'/check.json'
    url='https://drive.google.com/u/1/uc?id=1uGppiPKA6TF0Zxz3SjCnAp_5_0YsPXYF&export=download'
    gdown.download(url, output)
    with open(output, encoding="utf-8") as file:     #讀取寫入的文檔
        data = json.load(file)
    new_version=float(data['version'])
    version_info=data['update_info']
    version_state=data['state']
    global state
    
    if(data['activate']=='NO'):
        state=data['activate']
        return
    print(str(version_info))
    if (new_version>0.9):
        print("有新的版本"+str(new_version))
        version_info=version_info.replace("\\n","\n")
        ask=tkinter.messagebox.askquestion(title='更新', message="版本"+str(new_version)+version_state+"\n"+version_info)
        if ask=='yes':
            user_data=os.getenv('APPDATA')+r'\twiter_download/'
            print(user_data+'updata.exe')
            #win32api.ShellExecute(1, 'open', user_data+'update.exe', '', '',1)
            lockinput()
            try:
                print(data['update_exe'],data['update_exe_url'])
                if(float(data['update_exe'])>2.5):
                    url=data['update_exe_url']
                    exe=user_data+"updata.exe"
                    gdown.download(url,exe)
                    sleep(0.1)
                    while(1):
                        try:
                            win32api.ShellExecute(1, 'open', exe, '', '',1)
                            state='STOP'
                            return
                        except:
                            sleep(1)
                win32api.ShellExecute(0, 'open', user_data+r'/updata.exe', '', '',1)
                state='STOP'
            except Exception as err:
                print(err)
                print('找不到檔案，重新下載更新檔，請耐心等待')
                tkinter.messagebox.showinfo(title='警告', message='找不到檔案，重新下載更新檔，請耐心等待')
                url='https://drive.google.com/u/1/uc?id=10Jsyvr11wp9DT3oX9AbXdotwHYBZJqx8&export=download'
                exe=user_data+"update.exe"
                gdown.download(url,exe)
                sleep(0.1)
                while(1):
                    try:
                        win32api.ShellExecute(1, 'open', exe, '', '',1)
                        state='STOP'
                        break
                    except:
                        sleep(1)
        else:
            pass
    else:
        if (x==0):
            tkinter.messagebox.showinfo(title='通知', message='您使用的已經是最新版本了') 
    url='1ujpmREZXaNJy_QcZQgBllefSx_wG3HiQ'
def delthefile():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    root.destroy()
    thesamedel.del_the_same(path)
    tkinter.messagebox.showinfo(title='完成', message='刪除完成') 

def seticon():
    tama_img= tama.img
    user_data=os.getenv('APPDATA')+r'\twiter_download/'
    if os.path.isfile(user_data+'tama.ico'):
        pass
    else:
        ico = open(user_data+'tama.ico', 'wb+')
        ico.write(base64.b64decode(tama_img)) # 寫一個icon出來
        ico.close()
    window1.iconbitmap(user_data+'tama.ico')
    window2.iconbitmap(user_data+'tama.ico')
    '''try:
        os.remove(user_data+'tama.ico')
    except:
        pass'''
def setimg(root):
    user_data=os.getenv('APPDATA')+r'\twiter_download/'
    global img
    aqua_img=aqua.img
    aqua2_img=aqua2.img
    if os.path.isfile(user_data+'aqua.jpg'):
        pass
    else:
        ico = open(user_data+'aqua.jpg', 'wb+')
        ico.write(base64.b64decode(aqua_img)) # 寫一個icon出來
        ico.close()
    img= ImageTk.PhotoImage(Image.open(user_data+'aqua.jpg').resize((120, 120)))
    img_1= tk.Label(root,height=120,width=120,image = img).place(x=510, y=10)   
    
    global img2
    if os.path.isfile(user_data+'aqua2.jpg'):
        pass
    else:
        ico = open(user_data+'aqua2.jpg', 'wb+')
        ico.write(base64.b64decode(aqua2_img)) # 寫一個icon出來
        ico.close()
    img2= ImageTk.PhotoImage(Image.open(user_data+'aqua2.jpg').resize((120, 120)))
    img_2= tk.Label(root,height=120,width=120,image = img2).place(x=510, y=140)
    #img_open2=Image.open(user_data+'aqua2.ico')
    #img_open2=img_open2.resize((100,100))
    '''try:
        os.remove(user_data+'aqua.ico')
    except:
        pass'''
    
    
def setfunc():
    menu = Menu(window1)                 # 建立功能表物件
    filemenu = Menu(menu, tearoff=0)               # 建立檔案功能表
    menu.add_cascade(label="檔案",menu=filemenu)
    filemenu.add_command(label="刪除重複檔案",command=delthefile)
    filemenu.add_command(label="開啟使用者資訊",command=open_the_info_file)
    filemenu.add_command(label="檢查更新",command=update)
    filemenu.add_command(label="結束",command=close)
    filemenu = Menu(menu, tearoff=1)
    menu.add_cascade(label="關於",menu=filemenu)
    filemenu.add_command(label="版本資訊",command=about)
    window1.config(menu=menu)
def close():
    window1.destroy()
    window2.destroy()
def path():
    root = tk.Tk()
    root.withdraw()
    download_path = filedialog.askdirectory()
    root.destroy()
    var_usr_path.set(download_path)

def main_frame():
    window2.withdraw()
    window1.deiconify()
global info
info=''

def on_enter(i):
    info='下載線程數:'
    pL4String = tk.StringVar()
    pL4String.set("提高下載速度 但可能順序會亂掉")
    info = ttk.Label(window1,text = "提高下載速度 但可能順序會亂掉",foreground='#ff0000',font=('Arial', 16))
    info.place(x=200, y=265)
    window1.update()
def on_leave(i):
    info=''
    pL4String = tk.StringVar()
    pL4String.set("                                                      ")
    info = ttk.Label(window1,text = "                                                       ",font=('Arial', 16))
    info.place(x=200, y=265)
    window1.update()
global download_all_num,know_num
download_all_num=1
def update_bar():
    global download_all_num
    global download_num
    global check,know_num
    if(check==1):
        check=0
        go_main_frame['state']=tk.NORMAL
        return
    if(check==2):
        tk.Label(window2, text='正在抓取:'+str(know_num), font=('Arial', 14)).place(x=5,y=20)
    go_main_frame['state'] = tk.DISABLED   
    if(download_all_num==1):
        pass
    else :
        def get_current_value():                  # 傳回目前進度值之顯示字串
            return "目前進度 : " + str(round(progressbar["value"],2)) + "%" 
        tk.Label(window2, text='下載進度:', font=('Arial', 14)).place(x=5,y=70)
        var_bar=tk.StringVar()
        progressbar=ttk.Progressbar(window2, length=280, mode="determinate")   # 確定模式
        progressbar.place(x=115,y=75)
        progressbar["value"] = (download_num+1)/download_all_num*100
        bar=str(download_num+1)+"/"+str(download_all_num)
        #tk.Label(window2, text=bar, font=('Arial', 14)).place(x=450,y=250)
        tk.Label(window2, text=bar+" "+get_current_value(), font=('Arial', 14)).place(x=400,y=70)
    window2.update()
    window2.after(500,update_bar)
global state
state='None'
def run():
    global state
    if(state=='OK'):
        return 
    elif(state=='NO'):
        tkinter.messagebox.showinfo(title='Crash!!!', message='raise WebDriverException(selenium.common.exceptions.WebDriverException: \nMessage: coule not connect Internet \n Please contact the developer') 
        close()
    elif(state=='STOP'):
        close()
    elif(state=='None'):
        window1.after(500,run)
if __name__ == '__main__':
    
    user_log=(threading.Thread(target =update, args = (10,)))
    user_log.daemon = True 
    user_log.start()
    window1 =ttk.Window(title="twitter下載器",themename= "superhero",resizable=(False,False))
    window1.geometry("650x370+%d+%d"% ((window1.winfo_screenwidth()-610)/2,(window1.winfo_screenheight()-400)/2))
    run()
    window2 =ttk.Window(title="twitter下載器_正在運行",themename= "superhero",size=(610,300),resizable=(False,False))
    window2.geometry("650x210+%d+%d"% ((window1.winfo_screenwidth()-610)/2,(window1.winfo_screenheight()-210)/2))
    window2.withdraw()
    window1.protocol("WM_DELETE_WINDOW", close)#只要其中一個視窗關閉,就同時關閉兩個視窗
    window2.protocol("WM_DELETE_WINDOW", close)
    
    var_usr_address=tk.StringVar()
    var_usr_password=tk.StringVar()
    var_usr_url=tk.StringVar()
    var_usr_name=tk.StringVar()
    var_usr_path=tk.StringVar()
    b=tk.Button
    tk.Label(window1, text='帳號:', font=('Arial', 14)).place(x=12, y=12)
    tk.Label(window1, text='密碼:', font=('Arial', 14)).place(x=12, y=52)
    tk.Label(window1, text='網址:', font=('Arial', 14)).place(x=12, y=92)
    tk.Label(window1, text='用戶名:', font=('Arial', 14)).place(x=5, y=132)
    downloadpath = tk.Button(window1,text='路徑修改', font=('Arial', 12), width=7, height=1, command=path)
    downloadpath.place(x=1,y=172)
    usr_address = tk.Entry(window1, show=None,textvariable=var_usr_address, font=('Arial', 14))  # 顯示成明文形式
    usr_password = tk.Entry(window1, show='*',textvariable=var_usr_password, font=('Arial', 14))   # 顯示成密文形式
    url = tk.Entry(window1, show=None,textvariable=var_usr_url, font=('Arial', 14))   # 顯示成明文形式
    usr_name = tk.Entry(window1, show=None,textvariable=var_usr_name, font=('Arial', 14))
    usr_path = tk.Entry(window1, show=None,textvariable=var_usr_path, font=('Arial', 14))
    usr_address.place(x=85, y=15, width=400)
    usr_password.place(x=85, y=56, width=400)
    url.place(x=85, y=92, width=400)
    usr_name.place(x=85, y=132, width=400)
    usr_path.place(x=93, y=175, width=395)
    b = tk.Button(window1, text='開始', font=('Arial', 12),bg='#000000', width=10, height=1, command=begin)
    b.place(x=230,y=300)
    options=['1','2','3']
    tk.Label(window1, text='抓取速度:', font=('Arial', 14)).place(x=5, y=230)
    download_speed = ttk.Combobox(window1, 
                            values=[
                                    "自動",
                                    "快", 
                                    "普通",
                                    "慢",
                                    ],
                                    width='5',font=('Arial', 13))
    download_speed.current(0)
    download_speed.place(x=120,y=225)
    info_str=tk.Label(window1, text=info, font=('Arial', 14))
    info=tk.Label(window1, text='下載線程數:', font=('Arial', 14))
    info.place(x=230, y=230)
    info.bind("<Enter>", on_enter)
    info.bind("<Leave>", on_leave)
    download_thread_num = ttk.Combobox(window1, 
                            values=[  i for i in range(1,17) ]
                            ,font=('Arial', 14)
                            ,width='5')
    download_thread_num.current(0)
    download_thread_num.place(x=380,y=225)
    exit = tk.Button(window2, text='結束並離開', font=('Arial', 12), width=10, height=1, command=close)
    exit.place(x=520,y=150)
    go_main_frame = tk.Button(window2, text='回到下載頁面', font=('Arial', 12), width=13, height=1, command=main_frame)
    go_main_frame.place(x=20,y=150)
    know_num=tk.Label(window2, text='', font=('Arial', 14))
    
    seticon()
    app =setimg(window1)
    Userinfo()
    setfunc()    
    tk.mainloop()