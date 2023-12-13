當打開這份的時候 意味著忘了一些東西了

1.此為使用pyqt5開發的

2.要編譯.ui檔案  使用pyuic5 -x twitterdownload.ui -o UI.py

3.要設定icon 目前只能使用 pyrcc5 resource.qrc -o resource_rc.py
將其編譯為二進位檔案
<RCC>
  <qresource prefix="img">
    <file>logo.ico</file>
  </qresource>
</RCC>

然後在qtdesigner -> windowicon->theme裡貼入路徑"  :img/logo.ico    "

pyinstaller main.py -n twitter -D -w --icon D:\downloads\twitter_like_donwnload\logo.ico

打包用nsis
HM NIS Edit
https://blog.csdn.net/manongajie/article/details/107040212