import os
import json
import datetime
class data_format:
    def __init__(self):
        self.last_time_url = None
        self.previousLink = None
        self.usr_path = None
        self.tweet_id = None
        self.cookie = None
        self.download_path = None
        self.data_num = 0

class read_user_data(data_format):
    def __init__(self, user_data_path):
        super().__init__()
        self.user_data_path = user_data_path
        self.user_json = self.check_file()
        if len(self.user_json) == 0:
            return
        else:
            self.data_num = len(self.user_json)

    def check_file(self):
        if not os.path.isdir(self.user_data_path+"user_data"):
            os.mkdir(self.user_data_path+"user_data")
            return []
        else:
            return os.listdir(self.user_data_path+"user_data")    
        
    def read_info(self, num = -1):
        #讀取最新的json檔案
        if len(self.user_json) == 0:
            return data_format()
        else:
            file = open(self.user_data_path+"user_data/"+self.user_json[num], "r")
            jsonObject = json.load(file)
            file.close()
            data = data_format()
            data.last_time_url = jsonObject["last_time_url"]
            data.previousLink = jsonObject["previousLink"]
            data.usr_path = jsonObject["usr_path"]
            data.tweet_id = jsonObject["tweet_id"]
            data.cookie = jsonObject["cookie"]
            data.download_path = jsonObject["download_path"]
            return data

# class write_user_data:
#     def __init__(self, ):

#     def save_info(self):
#         jsonObject = {
            
#             # "password":  self.ui.password.text(),
#             "last_time_url": self.ui.last_url.text(),
#             "previousLink": self.previousLink,
#             "usr_path": self.ui.download_path.text(),
#             "download_thread_num": self.ui.download_thread_num.value(),
#             "exe_path": self.exe_path,
#             "tweet_id": self.tweet_id,
#             "cookie": self.ui.cookie.text(),
#         }
#         fileName = self.user_data_path+datetime.date.today().strftime("%Y_%m_%d.json")

#         with open(self.user_data_path+"json_recorder.txt", 'a+') as f:
#             f.write(fileName+'\n')
#         file = open(fileName, "w")
#         json.dump(jsonObject, file, indent=4)
#         file.close()
if __name__ == '__main__':
    user_data_path = os.path.join(os.getenv('APPDATA'), 'twitter_download')
    user_data=read_user_data(user_data_path)
    print(user_data.data_num)    