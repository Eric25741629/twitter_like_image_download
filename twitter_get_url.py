import re
from time import sleep
from PyQt5.QtCore import pyqtSignal,QThread
from functools import partial
import os
import json
import concurrent.futures
import twitter_url
from random import random
import requests
import datetime
#import glob

requests.packages.urllib3.disable_warnings()
class download_thread(QThread):
    _progressbar = pyqtSignal(int,int)
    _finish = pyqtSignal(int)
    _info_box = pyqtSignal(str,str)
    _err_box = pyqtSignal(str,str,int)
    address=''
    user_name=''
    last_url=''
    previousLink=''
    password=''
    download_path=''
    download_speed=''
    download_thread_num=0
    exe_path=''
    exist_img=set()
    urls=0
    driver=None
    user_data=os.getenv('APPDATA')+r'\twitter_download/'
    tweet_id=''
    headers = twitter_url.headers
    p_tw_link_text = re.compile(r'https://t.co/[\dA-Za-z]+$')
    p_csrf_token = re.compile(r'ct0=(.+?)(?:;|$)')
    pProxy = re.compile(r'.+?:(\d+)$')
    p_user_id = re.compile(r'"rest_id":"(\d+)"')
    p_twt_id = re.compile(r'conversation_id_str":"(\d+)')
    p_user_link = re.compile(r'https://twitter.com/([^/]+?)(?:/media)?$')
    p_twt_link = re.compile(r'https://twitter.com/(.+?)/status/(\d+)')
    get_pic_link =re.compile(r'''(https://pbs.twimg.com/media/(.+?))['"]''')
    p_gif_link = re.compile(r'(https://video.twimg.com/tweet_video/(.+?\.mp4))')
    p_vid_link = re.compile(
        r'(https://video.twimg.com/ext_tw_video/(\d+)/(?:pu|pr)/vid/(\d+x\d+)/(.+?\.mp4))')
    p_text_content = re.compile(r'''full_text['"]:\s?['"](.+?)['"]''')
    p_cursor = re.compile(r'value":"(.+?)"')
    def __init__(self,state='YES'):
        super(download_thread,self).__init__()
        self.read()
        self.onstate=state
        print(self.onstate)
        
    def save_info(self):
        jsonObject = {
        "username": self.user_name,
        "email": self.address,
        "password":  self.password,
        "last_time_url": self.last_url, 
        "previousLink": self.previousLink,
        "usr_path": self.download_path,
        "download_thread_num": self.download_thread_num,
        "exe_path":self.exe_path,
        "tweet_id":self.tweet_id,
        "cookie":self.headers['cookie'],
        "agent":self.headers['User-Agent'],
        }
        user_data=os.getenv('APPDATA')+r'\twitter_download/'
        fileName = user_data+datetime.date.today().strftime("%Y_%m_%d.json")
        with open(user_data+"json_recorder.txt", 'a+') as f:
            f.write(fileName+'\n')
        file = open(fileName, "w")
        json.dump(jsonObject, file, indent = 4)
        file.close()   

    def read(self):
        try:    
            user_data=os.getenv('APPDATA')+r'\twitter_download/'
            fileName = user_data+datetime.date.today().strftime("%Y_%m_%d.json")
            if os.path.isfile(fileName):
                with open(fileName) as f:
                    data = json.load(f)
                self.address=data['email']
                self.user_name=data['username']
                self.last_url=data['last_time_url']
                self.last_time_url=self.last_url
                self.password=data['password']
                self.download_path=data['usr_path']
                self.exe_path=data['exe_path']
                self.download_thread_num=int(data['download_thread_num'])
                self.previousLink=data['previousLink']
                try:
                    self.tweet_id=data['tweet_id']
                except:
                    self.tweet_id=None
                try:
                    self.headers['cookie']=data['cookie']
                except:
                    self._info_box.emit('錯誤','沒有取得cookies 請重新輸入')   
                self.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'
                self.headers['x-csrf-token']=self.p_csrf_token.findall(self.headers['cookie'])[0]
        except Exception as e:
            print(e)
            pass
    
    def state(self):
        if self.onstate =='NO':
            print('err')
            sleep(5)
            self._info_box.emit('錯誤','Traceback (most recent call last):  <br>File "d:/downloads/import tweepy1.py", line 1, in <module>    <br>from twitterscraper.query  <br>import query_user_info  <br>File "D:\python\envs\pkg_t\lib\site-packages\twitterscraper\__init__.py", line 13, in <module> <br>from twitterscraper.query import query_tweets  <br>File "D:\python\envs\pkg_t\lib\site-packages\twitterscraper\query.p    <br>proxies = get_proxies()  <br>File "D:\python\envs\pkg_t\lib\site-packages\twitterscraper\query.py", line 49, in get_proxies    <br>list_tr = table.find_all("tr")AttributeError: "NoneType" object has no attribute "find_all"   ')
            return 0
        return 1
    
    def get_token(self):
        #print(json.loads(requests.post(twitter_url.url_token, headers=self.headers).text))
        try:
            token = json.loads(requests.post(twitter_url.url_token, headers=self.headers).text)['guest_token']
            #print(token)
            self.headers['x-guest-token'] = token
        except:
            self._info_box.emit('錯誤','沒有取得token 請重新輸入cookies')
            return 0

    def getuserinfo(self,username,count=None):
        url = twitter_url.screename_url.format(username)
        userjson=requests.get(url, headers=self.headers).json()
        # print(userjson)
        if count==None:
            return(userjson['data']['user']['result']['rest_id']) 
        return(userjson['data']['user']['result']['rest_id'],userjson['data']['user']['result']['legacy']['favourites_count'])

    def first_get_url(self,response,get_twitter_id=None):
        media_url=[]
        get_media_url =  list(dict.fromkeys(self.get_pic_link.findall(response.text)))   #將所有圖片url使用正則表達法提取出來
        keep,media_url=self.add_url(media_url,get_media_url) #透過addurl將提取出來的圖片連結變成一個陣列
        new_cursor =  response.json()['data']['user']['result']['timeline_v2']['timeline']['instructions'][0]['entries'][-1]['content']['value'].replace('+',"%2B").replace('/',"%2F").replace('=','')
        if get_twitter_id!=None:
            twitter_id=set(self.p_twt_id.findall(response.text))
            return keep,media_url,new_cursor,twitter_id
        return keep,media_url,new_cursor
    
    def add_url(self,media_url,get_media_url):
        file_dict = {item[1]: item for item in get_media_url}
        if self.last_url not in file_dict:
            get_media_url = [url for url, filename in get_media_url]
            media_url= media_url+[i for i in get_media_url if i not in media_url]
            return 1,media_url
        for i in get_media_url:
            if i[1]==self.last_url:
                return 0,media_url
            media_url.append(i[0])
        return 0,media_url
    def get_url_and_cursor(self,user_id,new_cursor,media_url):
        response = requests.get(twitter_url.like_url.format(user_id,new_cursor), headers=self.headers)
        get_media_url =  list(dict.fromkeys(self.get_pic_link.findall(response.text)))
        print(get_media_url)
        keep,media_url=self.add_url(media_url,get_media_url)
        self._progressbar.emit(-1,len(media_url))
        #twitter_id=set.union(twitter_id,set(self.p_twt_id.findall(response.text)))
        p_cursor=new_cursor
        new_cursor =  response.json()['data']['user']['result']['timeline_v2']['timeline']['instructions'][0]['entries'][-1]['content']['value'].replace('+',"%2B").replace('/',"%2F").replace('=','')
        print(keep,p_cursor,new_cursor)
        return keep,p_cursor,new_cursor,media_url

    def error_test(self, response):
        '''如果錯誤 回傳0 '''
        try:
            if 'errors' in response.text:
                raise Exception('Cookies is not available')
            return 1
        except Exception as e:
            print(e)
            self._info_box.emit('錯誤','cookies 過期 重新獲取新的cookies')
            return 0
    
    def get_image_names(self,path: str):
        names = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png'):
                    names.append(os.path.splitext(file)[0])
        return names


    def new_func(self):
        if(self.onstate==0):
            return -1
        self.get_token()
        if self.last_url=='':
            user_id,like_count=self.getuserinfo(username=self.user_name.replace("@",''),count=1)
        else:
            user_id=self.getuserinfo(username=self.user_name.replace("@",'')) #獲得userid 
            self.last_url = re.search("https://pbs.twimg.com/media/(.*)(?:.*|\?.*)", self.last_url.replace("?format=",'.').replace(":orig",'').split('&name')[0]).group(1)#將上次的連結提取出圖片id
            like_count=100000000
        url=twitter_url.first_like_url.format(user_id)
        response =requests.get(url,headers=self.headers)
        if(not self.error_test(response)):
            return 
        keep,media_url,new_cursor,twitter_id=self.first_get_url(response,get_twitter_id='YES')
        while(keep):
            ''' 
            因為無法確定何時會停止 所以這邊使用while迴圈
            當要偵測到已有的時候 keep會變成0 終止無限迴圈
            '''
            keep,p_cursor,new_cursor,media_url=self.get_url_and_cursor(user_id,new_cursor,media_url)
            if(len(twitter_id)>=like_count or new_cursor==p_cursor):
                break
            sleep(0.3)
        download = media_url[::-1]
        self.urls=len(download)
        if download!=[]:
            self.exist_img=set(self.get_image_names(self.download_path+'/'))
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.download_thread_num) as self.executor:
                func=partial(self.download_twitter_img,self.download_path+'/')
                self.executor.map(func,download)
            self.previousLink=self.last_time_url
            self.last_url=media_url[0]
            self.save_info()
            self._finish.emit(1)
        else:
            self._finish.emit(-1)        
    
    def download_twitter_img(self, filepath, link):
        try:
            name = link.replace("https://pbs.twimg.com/media/", "").split(".")[0]
            if name in self.exist_img:
                self._progressbar.emit(1, self.urls)
                print('已下載過了')
                return 
            url = link
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            }
            #print(url)
            htmlfile = requests.get(url + ':orig', headers=headers,
                                    verify=False,
                                    stream=True,
                                    timeout=5)
            htmlfile.raise_for_status()
            size = 0
            chunk_size = 1024
            if ".jpg" in url:
                name += ".jpg"
            elif ".png" in url:
                name += ".png"
            
            # Use a generator to avoid creating a list of file names
            def get_file_names():
                yield filepath + name
                yield filepath + '1' + name
            
            # Use a for loop instead of a range loop to avoid creating an unused list
            for file_name in get_file_names():
                try:
                    with open(file_name, 'wb') as file:  
                        for data in htmlfile.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            size += len(data)
                    self._progressbar.emit(1, self.urls)
                    sleep(0.5)
                    return
                except Exception as err:
                    pass
                    #print(err)

        except Exception as err:
            pass
        return
    
    # def download_twitter_img(self,filepath,link):
    #     try:
    #         for i in range(0,3):
    #             name=link.replace("https://pbs.twimg.com/media/","").split(".")[0]
    #             url=link
    #             headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
    #                         }
    #             print(url)
    #             htmlfile = requests.get(url,headers=headers,verify=False,stream=True,timeout=5)
    #             htmlfile.raise_for_status() 
    #             size = 0
    #             chunk_size = 1024
    #             if ".jpg"in url:
    #                 name=name+".jpg"
    #             elif ".png"in url:
    #                 name=name+".png"
    #             try:
    #                 with open(filepath+name,'wb') as file: 
    #                     for data in htmlfile.iter_content(chunk_size = chunk_size):
    #                         file.write(data)
    #                         size +=len(data)  
    #                 self._progressbar.emit(1,self.urls)
    #                 sleep(1)
    #                 return
    #             except:
    #                 try:
    #                     with open(filepath+'1'+name,'wb') as file: 
    #                             for data in htmlfile.iter_content(chunk_size = chunk_size):
    #                                 file.write(data)
    #                                 size +=len(data) 
    #                 except Exception as err:
    #                     print(err)
    #                     pass
                        
    #             break
    #     except Exception as err:
    #         print(err)
    #         pass
        
    #     return 

    def run(self):
        #import tweepy
        # self.getcookies()
        self.new_func()
        # if(self.state()==0):
        #     #self._info_box.emit('錯誤','Traceback (most recent call last):  <br>File "d:/downloads/import tweepy1.py", line 1, in <module>    <br>from twitterscraper.query  <br>import query_user_info  <br>File "D:\python\envs\pkg_t\lib\site-packages\twitterscraper\__init__.py", line 13, in <module> <br>from twitterscraper.query import query_tweets  <br>File "D:\python\envs\pkg_t\lib\site-packages\twitterscraper\query.p    <br>proxies = get_proxies()  <br>File "D:\python\envs\pkg_t\lib\site-packages\twitterscraper\query.py", line 49, in get_proxies    <br>list_tr = table.find_all("tr")AttributeError: "NoneType" object has no attribute "find_all"   ')
        #     return  
        # download=[]
        # bearer_token = "Bearer AAAAAAAAAAAAAAAAAAAAAEzicAEAAAAA6EZ%2BpsMWNmEaFEKsSDFqtmAU%2Bco%3DTA3yElQF4FLT2MRNd2cA70nu7xoknZ7ZqtORtmytmQ9thkvF1A"
        # token =               "AAAAAAAAAAAAAAAAAAAAAEzicAEAAAAA6EZ%2BpsMWNmEaFEKsSDFqtmAU%2Bco%3DTA3yElQF4FLT2MRNd2cA70nu7xoknZ7ZqtORtmytmQ9thkvF1A"
        # headers={'Authorization':bearer_token}
        # client = tweepy.Client(token,wait_on_rate_limit=True)
        # twitter_id=[]
        # user_id=client.get_user(username=self.user_name.replace("@",'')).data.id
        # print(user_id)
        # token=None
        # state=1
        # while(1):
        #     try:
        #         response = client.get_liked_tweets(user_id, tweet_fields=["created_at"],max_results=100,pagination_token=token)
        #         print(response)
        #         if(response.data==None):
        #             break 
        #         for tweet in response.data:
        #             self._progressbar.emit(-1,len(twitter_id))
        #             if(self.tweet_id!=None):
        #                 if (tweet.id==int(self.tweet_id)):
        #                     state=0
        #                     break  
        #             twitter_id.append(tweet.id)
        #         if state==0:break
        #         token=response.meta['next_token']
        #         print(token)
        #     except:
        #         print(response)
        #     sleep(1)   
        # if  twitter_id==[]:
        #     self._finish.emit(-1)
        #     return 
        # self.tweet_id=str(twitter_id[0])    

        # # 將ID分成多組
        # string = [twitter_id[i:i+100] for i in range(0, len(twitter_id), 100)]
        # match = re.search("https://pbs.twimg.com/media/(.*)(?:\.|\?.*)", self.last_url)
        # if match:
        #     last_url = match.group(1)
        # else:
        #     last_url='NONENONONOONONNONONONONONONONONONONOONONONO'
        # state=1
        # for i in range(0,len(string)):
        #     ids=string[i]
        #     twitteridstr=''
        #     for id in ids:
        #         if twitteridstr !='':
        #             twitteridstr=twitteridstr+','+str(id)
        #         else:
        #             twitteridstr=str(id)
        #     url=('https://api.twitter.com/2/tweets?ids={}&tweet.fields=lang&expansions=attachments.media_keys&media.fields=url'.format(twitteridstr))
        #     print(url)
        #     i=requests.get(url,headers=headers)
        #     try:
        #         media_list=i.json()['includes']['media']
        #         for media in media_list:
        #             try:
        #                 #print(media['url'])
        #                 link=media['url']
        #                 name=link.replace("https://pbs.twimg.com/media/","").split(".")[0]
        #                 url=link+":orig"
        #                 download.append(url)
        #                 if(last_url in name):
        #                     state=0
        #                     break
        #             except:
        #                 pass
        #     except:
        #         pass
        #     if (state==0):
        #         break
        #     self._progressbar.emit(3,len(string))
        # self.urls=len(download)
        # self._progressbar.emit(2,self.urls)
        # download = download[::-1]
        
        # if download!=[]:
        #     with concurrent.futures.ThreadPoolExecutor(max_workers=self.download_thread_num) as self.executor:
        #         func=partial(self.download_twitter_img,self.download_path+'/')
        #         self.executor.map(func,download)
        #     self.previousLink=self.last_url
        #     self.last_url=download[0]
        #     self.save_info()
        #     self._finish.emit(1)
        # else:
        #     self._finish.emit(-1)
    
  
  
