import os
from socket import dup
import numpy as np
import time
from PIL import Image,ImageChops
from collections import Counter  
#采用SSIM进行对比，速度会较慢

#采用PIL中的Imagecrops进行对比，速度会快上很多
def found_same_img_2(path):
    '''oldest=0
    oldest_path=''
    for i in range(0,len(path)):
        times=os.path.getmtime(path[i][0]+path[i][1])
        if i==0 or times<oldest:
            oldest=times
            oldest_path=path[i][0]+path[i][1]
            num=i
        if times==oldest:
            if(len(oldest_path)>len(path[i][0]+path[i][1])):
                oldest_path=path[i][0]+path[i][1]
                num=i
    print(num)'''
    print(path)
    for i in range(0,len(path)):
        # start=time.time()
        try:
            img=Image.open((path[i][0]+path[i][1])).resize((100,100))
            times1=os.path.getmtime(path[i][0]+path[i][1])
            for other_img_dir in range(i+1,len(path)):
                # other_img=cv2.imread(other_img_dir)
                other_img =Image.open(path[other_img_dir][0]+path[other_img_dir][1]).resize((100,100))
                # print(img_dir,other_img_dir)
                try:
                    if(np.array_equal(img, other_img)):
                        #print('Same:',path[i][0]+path[i][1], '----', path[other_img_dir][0]+path[other_img_dir][1])
                        try:
                            times2=os.path.getmtime(path[other_img_dir][0]+path[other_img_dir][1])
                            if times1<times2:
                                os.remove(path[other_img_dir][0]+path[other_img_dir][1])
                            elif times1>times2:
                                os.remove(path[i][0]+path[i][1])
                            elif times1==times2:
                                if(len(path[i][0]+path[i][1])>len(path[other_img_dir][0]+path[other_img_dir][1])):
                                    os.remove(path[i][0]+path[i][1])
                                else:
                                    os.remove(path[other_img_dir][0]+path[other_img_dir][1])
                        except Exception as err:
                            print(err)
                except:
                    #print('Error,图片不匹配:',path[i][0]+path[i][1], '----',path[other_img_dir][0]+path[other_img_dir][1])
                    continue
            # finish=time.time()
            # print(No,'  Time:',round((finish-start),2))
            print('次数:',i)
        except Exception as err:
            print(err)
            break
def get_filelist(path):
    Filelist = []
    for home, dirs, files in os.walk(path):
        for filename in files:
            # 文件名列表，包含完整路徑
            Filelist.append((home, filename))
    return Filelist
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
from multiprocessing import Process
from multiprocessing import Pool, cpu_count
if __name__ == '__main__':
    path=r'D:\tst/'
    all_the_same_imgs=byte_same(path)

    if all_the_same_imgs!=[]:
        print('12')    
        thread_pool = Pool(int(cpu_count()/4))
        result_list = thread_pool.map(found_same_img_2, all_the_same_imgs)
        thread_pool.close()
        thread_pool.join()
    '''for i in range(0,len(all_the_same_imgs)):
        found_same_img_2(all_the_same_imgs[i])'''
        #p = Process(target=found_same_img_2, args=(all_the_same_imgs[i],))
        

        
    '''    p.start()
    p.join()'''
	#found_same_img_2(path)