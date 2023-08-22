#timetest
import os,time,datetime
start=time.time()
for i in range(100):
    user_data=os.getenv('APPDATA')+r'\twitter_download/'
    fileName = user_data+datetime.date.today().strftime("%Y_%m_%d.json")
stop=time.time()
print(stop-start)