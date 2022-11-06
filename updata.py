from ensurepip import version
import os,gdown,tkinter
from tkinter import messagebox
import subprocess,win32api,json

def writedata(address,password,link,user_name,download_path,lastlink='none',exe_path='none',version=0):
    f = open((user_data+"password.txt"), "w+")
    f.write(address+"\n")
    f.write(password+"\n")
    f.write(link+"\n")
    f.write(user_name+"\n")
    f.write(download_path+"\n")
    f.write(lastlink+"\n")
    f.write(exe_path+"\n")
    f.write(version+"\n")
    f.close()
print('正在獲取更新網址')
user_data=os.getenv('APPDATA')+r'\twiter_download/'
if os.path.isfile(user_data+'data.json'):
    with open(user_data+'data.json') as f:
        data = json.load(f)
    address=data['email']
    user_name=data['username']
    link=data['last_time_url']
    password=data['password']
    download_path=data['usr_path']
    exe_path=data['exe_path']
    download_speed=data['download_speed']
    download_thread_num=data['download_thread_num']
    last_last_time_url=data['last_last_time_url']
    url='https://drive.google.com/u/1/uc?id=1ujpmREZXaNJy_QcZQgBllefSx_wG3HiQ&export=download'
    update=user_data+r'/check.json'
    output=exe_path+r'/twitter.exe'
    gdown.download(url, output)
    fileName = user_data+"data.json"
    top=tkinter.Tk()
    top.geometry('0x0+999999+0')
    ask=tkinter.messagebox.askquestion(title='完成', message='是否開啟')
    if ask=='yes':
        win32api.ShellExecute(0, 'open', output, '', '',0)
    else:
        pass
    top.destroy()
else:
    pass