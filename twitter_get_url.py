import re
from time import sleep
from PyQt5.QtCore import pyqtSignal, QThread
from functools import partial
import os
import json
import concurrent.futures
import twitter_url
from random import random
import requests
import datetime
# import glob
from write_and_read_json import user_data
requests.packages.urllib3.disable_warnings()


class get_twitter_info(twitter_url.twitter_link_regex):
    def __init__(self, headers):
        self.headers = headers

    def get_token(self):
        try:
            token = json.loads(requests.post(
                twitter_url.url_token, headers=self.headers).text)['guest_token']
            return token
            # headers['x-guest-token'] = token
        except:
            return 'error'

    def get_user_info(self, username, get_count_num=False):
        url = twitter_url.screename_url.format(username)
        userjson = requests.get(url, headers=self.headers)
        print(userjson)
        userjson = userjson.json()
        if get_count_num:
            return (userjson['data']['user']['result']['rest_id'], userjson['data']['user']['result']['legacy']['favourites_count'])
        return (userjson['data']['user']['result']['rest_id']), None

    def get_tweetids_and_cursor(self, user_id, cursor=None):
        if cursor == None:
            url = twitter_url.first_like_url.format(user_id)
        else:
            url = twitter_url.like_url.format(user_id, cursor)
        response = requests.get(url, headers=self.headers)
        get_media_url = list(dict.fromkeys(
            self.get_pic_link.findall(response.text)))
        twitter_ids = set(self.p_twt_id.findall(response.text))
        last_cursor = cursor
        cursor = response.json()['data']['user']['result']['timeline_v2']['timeline']['instructions'][0]['entries'][-1]['content']['value'].replace(
            '+', "%2B").replace('/', "%2F").replace('=', '')
        return twitter_ids, get_media_url, cursor, last_cursor

    def error_test(self, response):
        '''如果錯誤 回傳0 '''
        try:
            if 'errors' in response.text:
                # return False
                raise Exception('Cookies is not available')
            else:
                return True

        except Exception as e:
            print(e)
            return False

    def test_cookies(self, url):
        url = 'https://twitter.com/home'
        response = requests.get(url, headers=self.headers)
        return self.error_test(response)


class download_thread(QThread, twitter_url.twitter_link_regex):
    _progressbar = pyqtSignal(int, int)
    _finish = pyqtSignal(int)
    _info_box = pyqtSignal(str, str)
    _err_box = pyqtSignal(str, str, int)
    exist_img = set()
    urls = 0
    usr_path = os.getenv('APPDATA')+r'\twitter_download/'
    tweet_id = ''
    headers = twitter_url.headers

    def __init__(self, usrdata: user_data):
        super(download_thread, self).__init__()
        self.usrdata = usrdata
        self.headers['cookie'] = self.usrdata.cookie
        self.usr_name = self.usrdata.usr_name.replace("@", '')
        self.request_twitter = get_twitter_info(self.headers,)
        self.last_time_url = self.usrdata.last_time_url

    def add_url(self, get_media_url, media_url=[]):
        file_dict = {item[1]: item for item in get_media_url}
        if self.last_time_url not in file_dict:
            get_media_url = [url for url, filename in get_media_url]
            media_url = media_url + \
                [i for i in get_media_url if i not in media_url]
            return media_url, True
        else:
            for i in get_media_url:
                if i[1] == self.last_time_url:
                    return media_url, False
                media_url.append(i[0])
            print('找到上次的連結')
            return media_url, False

    def get_image_names(self, path: str):
        names = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png'):
                    names.append(os.path.splitext(file)[0])
        return names

    def get_all_img_url(self):

        token = self.request_twitter.get_token()
        if token == 'error':
            self._info_box.emit('錯誤', '沒有取得token 請重新輸入cookies')
            return
        self.headers['x-guest-token'] = token
        self.request_twitter.headers = self.headers
        user_id, like_count = self.request_twitter.get_user_info(
            self.usr_name, get_count_num=True)  # 獲得userid

        if self.usrdata.last_time_url == '':
            print('沒有上次的連結')
            self.last_time_url = ''
        else:
            self.last_time_url = re.search("https://pbs.twimg.com/media/(.*)(?:.*|\?.*)", self.usrdata.last_time_url.replace(
                "?format=", '.').replace(":orig", '').split('&name')[0]).group(1)  # 將上次的連結提取出圖片id
        if self.request_twitter.test_cookies(twitter_url.first_like_url.format(user_id)):
            # log.write_log('info', 'cookies is available')
            pass
        else:
            self._info_box.emit('錯誤', 'cookies is not available')
            # log.write_log('info', 'cookies is available')
            return
        twitter_ids, get_media_url, cursor, last_cursor = self.request_twitter.get_tweetids_and_cursor(
            user_id=user_id)
        img_urls, continue_ = self.add_url(get_media_url)
        all_img_urls = img_urls
        while continue_:
            twitter_ids, get_media_url, cursor, last_cursor = self.request_twitter.get_tweetids_and_cursor(
                user_id=user_id, cursor=cursor)
            img_urls, continue_ = self.add_url(get_media_url)
            all_img_urls += img_urls
            sleep(0.3)
            self._progressbar.emit(-1, len(all_img_urls))
            if cursor == last_cursor or len(all_img_urls) >= like_count:
                break
        all_img_urls = all_img_urls[::-1]
        self.urls = len(all_img_urls)
        return all_img_urls

    def run(self):
        all_img_urls = self.get_all_img_url()
        if all_img_urls != []:
            self.exist_img = set(self.get_image_names(
                self.usrdata.download_path+'/'))
            # self.exist_img = set()
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.usrdata.download_thread_num) as self.executor:
                func = partial(self.download_twitter_img,
                               self.usrdata.download_path+'/')
                self.executor.map(func, all_img_urls)
            self.previousLink = self.usrdata.last_time_url
            self.usrdata.last_time_url = all_img_urls[-1]
            self.usrdata.save_info()
            self._finish.emit(1)
        else:
            self._finish.emit(-1)

    def download_twitter_img(self, filepath, link):
        try:
            # Extracting image name from the link
            name = self.extract_image_name(link)
            if name in self.exist_img:
                self._progressbar.emit(1, self.urls+1)
                print('已下載過了')
                return
            # Downloading image
            self.download_image(filepath, name, link)
        except Exception as err:
            pass

    def extract_image_name(self, link):
        return link.replace("https://pbs.twimg.com/media/", "").split(".")[0]

    def download_image(self, filepath, name, link):
        try:
            url = link + ':orig'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            }
            response = requests.get(
                url, headers=headers, verify=False, stream=True, timeout=5)
            response.raise_for_status()

            # Determine file extension based on URL
            if ".jpg" in url:
                name += ".jpg"
            elif ".png" in url:
                name += ".png"

            # Download the image
            file_path = filepath + name
            self.save_image(response, file_path)
        except Exception as err:
            pass

    def save_image(self, response, file_path):
        try:
            size = 0
            chunk_size = 1024
            with open(file_path, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
            self._progressbar.emit(1, self.urls)
            sleep(0.5)
        except Exception as err:
            pass


if __name__ == '__main__':
    path = os.getenv('APPDATA')+r'\twitter_download/'
    usr_data = user_data()
    usr_data.read_info(0)
    download_thread(usr_data).run()
