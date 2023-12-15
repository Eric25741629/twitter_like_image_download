import os
import json
import datetime


class data_format:
    last_time_url: str
    previousLink: str = ''
    usr_path: str
    usr_name: str
    tweet_id: str
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
            self.tweet_id = jsonObject["tweet_id"]
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
            "tweet_id": self.tweet_id,
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
    # def get_user_json(self):
    #     try:
    #         data_list = (glob.glob(os.path.join(
    #             self.user_data_path, "*.json")))
    #         with open(self.user_data_path+"json_recorder.txt", 'w') as file:
    #             for i in data_list:
    #                 path = i.rsplit('\\', 1)
    #                 file.write(path[0]+'/'+path[1]+'\n')
    #     except:
    #         pass
    #     try:
    #         with open(self.user_data_path+"json_recorder.txt", 'r') as file:
    #             lines = [line.rstrip() for line in file]
    #         lines = list(dict.fromkeys(lines))
    #         with open(self.user_data_path+"json_recorder.txt", 'w') as file:
    #             for i in lines:
    #                 file.write(i+'\n')
    #         self.recorder = lines[::-1]
    #         self.show_recorder = [i.split('/')[1] for i in self.recorder]
    #         # print(self.recorder)
    #         self.ui.use_data.addItems(self.show_recorder)
    #     except:
    #         pass

    # def load_user_data(self):
    #     try:
    #         try:
    #             if (self.ui.use_data.currentIndex() == -1):
    #                 pre = 0
    #             else:
    #                 pre = self.ui.use_data.currentIndex()
    #         except:
    #             pre = 0
    #         # print(pre)
    #         # print(self.recorder[pre])
    #         if os.path.isfile(self.recorder[pre]):
    #             with open(self.recorder[pre]) as f:
    #                 data = json.load(f)
    #             print(data['email'])

    #             self.last_url = data['last_time_url']
    #             self.password = data['password']
    #             self.download_path = data['usr_path']
    #             self.exe_path = data['exe_path']
    #             self.download_thread_num = int(data['download_thread_num'])
    #             self.previousLink = data['previousLink']
    #             try:
    #                 self.tweet_id = data['tweet_id']
    #                 print(self.tweet_id)
    #             except Exception as err:
    #                 print(err)
    #                 self.tweet_id = None
    #             try:
    #                 self.cookie = data['cookie']
    #                 self.agent = data['agent']
    #             except:
    #                 pass
    #         else:
    #             print('no find')
    #         self.ui.address.setText(self.address)
    #         self.ui.password.setText(self.password)
    #         self.ui.last_url.setText(self.last_url)
    #         self.ui.user_name.setText(self.user_name)
    #         self.ui.download_path.setText(self.download_path)
    #         self.ui.cookie.setText(self.cookie)
    #         # self.ui.download_speed.setCurrentText(download_speed)
    #         self.ui.download_thread_num.setValue(self.download_thread_num)
    #     except Exception as e:
    #         output_err(e)
    #         pass

    # def the_first_use(self):
    #     if os.path.isfile(self.user_data_path+'data.json'):
    #         time = (datetime.date.today()-datetime.timedelta(days=1)
    #                 ).strftime("%Y_%m_%d.json")
    #         os.rename(self.user_data_path+'data.json',
    #                   self.user_data_path+time)
    #         with open(self.user_data_path+"json_recorder.txt", 'a+') as f:
    #             f.write(self.user_data_path+time+'\n')


if __name__ == '__main__':
    user_data_path = os.path.join(os.getenv('APPDATA'), 'twitter_download')
    usr_data = user_data(user_data_path)
    print(usr_data.user_json)
    usr_json_name = [i.split('.')[0] for i in usr_data.user_json]
    print(usr_json_name)
