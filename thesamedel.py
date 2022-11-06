import os,time
from operator import itemgetter, attrgetter
import hashlib
import numpy as np
from tqdm import tqdm, trange
import shutil
from PIL import Image,ImageChops
from tkinter import Tk,filedialog
from collections import Counter  
from multiprocessing import Pool, cpu_count
def byte_same(path):
    list1=get_filelist(path)
    bytelist=[]
    for i in range(0,len(list1)):
        byte=os.path.getsize(list1[i][0]+"/"+list1[i][1])
        bytelist.append(byte)
    print(bytelist)
    result = Counter(bytelist)
    most_common = result.most_common()
    duplicate=[i[0] for i in most_common if i[1]>1]     #在most_common裡面循環 假設i[1]大於1 就加入陣列裡
    result=[]
    for i in duplicate:
        img_path = [list1[j][0] for j in np.where(np.array(bytelist) == i)[0]]
        img_name = [list1[j][1] for j in np.where(np.array(bytelist) == i)[0]]
        z = list(zip(img_path,img_name))
        result.append(z)
    return result

def get_filelist(path):
    Filelist = []
    for home, dirs, files in os.walk(path):
        for filename in files:
            # 文件名列表，包含完整路徑
            Filelist.append((home, filename))
    return Filelist
def sha_256(file):
    img=open(file,"rb")
    #file_txt = open(file, 'rb').read()
    m = hashlib.sha256(img.read())
    return m.hexdigest()
#def usa_sha256_and_datatime_to_del(file):
def del_the_same(imgs):
    sha_256_list=[sha_256(i[0]+i[1]) for i in imgs]
    print(sha_256_list)
    for i in range(0,len(sha_256_list)):
        for j in range(i+1,len(sha_256_list)):
            if sha_256_list[i]==sha_256_list[j]:
                try:
                    i_time=os.path.getmtime(imgs[i][0]+imgs[i][1])
                    j_time=os.path.getmtime(imgs[j][0]+imgs[j][1])
                    if i_time>j_time:
                        os.remove(imgs[j][0]+imgs[j][1])   
                    elif i_time<j_time:
                        os.remove(imgs[i][0]+imgs[i][1])  
                    elif i_time==j_time:
                        if(len(imgs[i][0]+imgs[i][1])>len(imgs[j][0]+imgs[j][1])):
                            os.remove(imgs[i][0]+imgs[i][1])  
                        elif(len(imgs[i][0]+imgs[i][1])<len(imgs[j][0]+imgs[j][1])):
                            os.remove(imgs[j][0]+imgs[j][1])
                except Exception as err:
                    pass
                    #print(err)

def main_the_same_del(path):
    #list1=get_filelist(path)
    total_the_same_img=byte_same(path)
    print(total_the_same_img[0])
    thread_pool = Pool(int(cpu_count()/4))
    result_list = thread_pool.map(del_the_same, total_the_same_img)
    thread_pool.close()
    thread_pool.join()
if __name__ == '__main__':
    main_the_same_del(r'D:\test/')
