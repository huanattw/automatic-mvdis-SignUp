# mvids_motercycle_signUp

## Introduction
最近朋友開始搶機車駕照，所以就幫忙寫惹

## Depndencies
* requests
* bs4 
* lxmllxml

## Usage 
1. 下載到電腦
 ```shell
 git clone https://github.com/mhy1264/mvdis_bot.git
 ```
 
2. 安裝套件
```
pip install requests bs4 lxml
```

3. 新增 accounts.ini 存放個人基本資料、LineNotifyToken 的檔案，格式如下:<br>
Line Notify Token 可以參考 : [自建 LINE Notify 訊息通知](https://www.oxxostudio.tw/articles/201806/line-notify.html)
```
[Default]
id = 身份證字號
birth = YYYMMDD (YYY是民國年)
name = 姓名
phone = 電話
email = 電子信箱
token = LineNotifyToken
```

4. 更改 監理所(站)代碼
這個代碼有空我會補上
```python
self.location[60,64] # 這裡的60 是監理站的代碼 64是監理所的代碼
```

5. 執行
```
python mvids.py
```
> **Warning** <br>
> 請斟酌使用本機器人程式，並自行負責使用後所造成的損失!
