import os
import json
import datetime


class data_format:
    last_time_url: str
    previousLink: str = ''
    usr_path: str
    usr_name: str
    tweet_id: str = None
    cookie: str
    download_path: str
    data_num: int
    download_thread_num: int
    user_json: list
    show_recorder: list


class user_data(data_format):
    def __init__(self, user_data_path=os.path.join(
            os.getenv('APPDATA'), 'twitter_download')):
        super(data_format).__init__()
        self.user_data_path = user_data_path
        self.user_json = self.check_file()
        if len(self.user_json) == 0:
            print("No user data")
            self.data_num = 0
        else:
            # 將user_json倒序排列
            self.user_json = self.user_json[::-1]
            self.data_num = len(self.user_json)
            self.read_info()
            self.show_recorder = [i.split('.')[0] for i in self.user_json]

    def check_file(self):
        if not os.path.isdir(self.user_data_path+"/user_data"):
            os.mkdir(self.user_data_path+"/user_data")
            return []
        else:
            return os.listdir(self.user_data_path+"/user_data")

    def read_info(self, num=0):
        # 讀取最新的json檔案
        if len(self.user_json) == 0:
            return False
        else:
            file = open(self.user_data_path+"/user_data/" +
                        self.user_json[num], "r")
            jsonObject = json.load(file)
            file.close()
            self.usr_name = jsonObject["usr_name"]
            self.last_time_url = jsonObject["last_time_url"]
            self.previousLink = jsonObject["previousLink"]
            # self.tweet_id = jsonObject["tweet_id"]
            self.cookie = jsonObject["cookie"]
            self.download_path = jsonObject["download_path"]
            self.download_thread_num = jsonObject["download_thread_num"]
            return True

    def save_info(self):
        jsonObject = {
            "usr_name": self.usr_name,
            "last_time_url": self.last_time_url,
            "previousLink": self.previousLink,
            "download_path": self.download_path,
            # "tweet_id": self.tweet_id,
            "cookie": self.cookie.replace('\n', ''),
            "download_thread_num": self.download_thread_num,
        }
        fileName = self.user_data_path+"/user_data/" + \
            datetime.date.today().strftime("%Y_%m_%d.json")
        # with open(self.user_data_path+"json_recorder.txt", 'a+') as f:
        #     f.write(fileName+'\n')
        file = open(fileName, "w")
        json.dump(jsonObject, file, indent=4)
        file.close()


if __name__ == '__main__':
    user_data_path = os.path.join(os.getenv('APPDATA'), 'twitter_download')
    usr_data = user_data(user_data_path)
    print(usr_data.user_json)
    usr_json_name = [i.split('.')[0] for i in usr_data.user_json]
    print(usr_json_name)
