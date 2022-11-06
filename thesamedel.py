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
    #print(total_the_same_img)
    #for i in trange(0,len(total_the_same_img)):

    '''finallist=shalist=[]
        for j in totalbytelist[i]:
            file=bytelist[j][0]+"/"+bytelist[j][1]
            #sha_256(file)
            shalist.append([bytelist[j][0],bytelist[j][1],sha_256(file)])
        shalist=sorted(shalist, key = itemgetter(1))
        lenth=0
        while(1):
            if lenth>=len(shalist):
                break            
            #print(shalist[lenth][1])
            shalist=np.array(shalist)
            eq_letter=np.argwhere(shalist==shalist[lenth][2])
            lenth=lenth+1
            if len(eq_letter)<2:     
                continue
            lenth=lenth+len(eq_letter)-1
        num=0    
        photo_time=0
        the_next_photo=0
        #eq_letter=np.unique(eq_letter,axis=0)
        if len(eq_letter)>1:
            while(1):
                try:
                    if num>=len(eq_letter):
                        break 
                    #print(shalist[eq_letter[num][0]][0]+"\n"+shalist[eq_letter[num][0]][1]+"\n",num)
                    
                    if photo_time==0:
                        photo_time=(os.path.getmtime(shalist[eq_letter[num][0]][0]+"/"+shalist[eq_letter[num][0]][1]),num)
                    else:
                        the_next_photo=(os.path.getmtime(shalist[eq_letter[num][0]][0]+"/"+shalist[eq_letter[num][0]][1]),num)
                        if photo_time[0]>the_next_photo[0]:
                            os.remove(shalist[eq_letter[photo_time[1]][0]][0]+"/"+shalist[eq_letter[photo_time[1]][0]][1])
                            photo_time=the_next_photo
                        elif photo_time[0]<the_next_photo[0]:
                            os.remove(shalist[eq_letter[num][0]][0]+"/"+shalist[eq_letter[num][0]][1])
                        elif photo_time[0]==the_next_photo[0]:
                            if (len(shalist[eq_letter[photo_time[1]][0]][1])>len(shalist[eq_letter[num][0]][1])):
                                os.remove(shalist[eq_letter[photo_time[1]][0]][0]+"/"+shalist[eq_letter[photo_time[1]][0]][1])
                                photo_time=the_next_photo
                            else:
                                os.remove(shalist[eq_letter[num][0]][0]+"/"+shalist[eq_letter[num][0]][1])
                except:
                    pass                
                num=num+1'''
if __name__ == '__main__':
    main_the_same_del(r'D:\test/')
'''for i in trange(0,len(shalist)):
        if shalist[i][2]'''
    
'''if num>=len(eq_letter):
                    break 
                #print(shalist[eq_letter[num][0]][0]+"\n"+shalist[eq_letter[num][0]][1]+"\n")
                try:
                    if photo_time==0:
                        photo_time=(os.path.getmtime(shalist[eq_letter[num][0]][0]+"/"+shalist[eq_letter[num][0]][1]),num)
                    else:
                        the_next_photo=(os.path.getmtime(shalist[eq_letter[num][0]][0]+"/"+shalist[eq_letter[num][0]][1]),num)
                        if photo_time[0]>the_next_photo[0]:
                            #shutil.move(shalist[eq_letter[photo_time[1]][0]][0]+"/"+shalist[eq_letter[photo_time[1]][0]][1],r'D:\重複/'+shalist[eq_letter[photo_time[1]][0]][1])
                            os.remove(shalist[eq_letter[photo_time[1]][0]][0]+"/"+shalist[eq_letter[photo_time[1]][0]][1])
                            photo_time=the_next_photo
                        elif photo_time[0]>the_next_photo[0]:
                            #shutil.move(shalist[eq_letter[num][0]][0]+"/"+shalist[eq_letter[num][0]][1],r'D:\重複/'+shalist[eq_letter[num][0]][1])
                            os.remove(shalist[eq_letter[photo_time[1]][0]][0]+"/"+shalist[eq_letter[photo_time[1]][0]][1])
                            
                        elif photo_time[0]==the_next_photo[0]:
                            if (len(shalist[eq_letter[photo_time[1]][0]][1])>len(shalist[eq_letter[num][0]][1])):
                                os.remove(shalist[eq_letter[photo_time[1]][0]][0]+"/"+shalist[eq_letter[photo_time[1]][0]][1])
                                #shutil.move(shalist[eq_letter[photo_time[1]][0]][0]+"/"+shalist[eq_letter[photo_time[1]][0]][1],r'D:\重複/'+shalist[eq_letter[photo_time[1]][0]][1])
                                photo_time=the_next_photo
                            else:
                                os.remove(shalist[eq_letter[photo_time[1]][0]][0]+"/"+shalist[eq_letter[photo_time[1]][0]][1])
                                #shutil.move(shalist[eq_letter[num][0]][0]+"/"+shalist[eq_letter[num][0]][1],r'D:\重複/'+shalist[eq_letter[num][0]][1])
                except Exception as err:
                    print(err)'''