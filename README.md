591 租屋網資訊API
==================

## 說明
給他一個 591 的網址，他會將租屋資訊轉成 JSON 格式給你，同時支援抓取連絡電話。提供一個 cli 工具以及一個基於 flask 的 api 介面。

## 使用方式
### 安裝
1. 先 clone 一份 repo 到本地端
```sh
git clone https://github.com/frankurcrazy/591HousingApi.git
cd 591HousingApi
```

2. 安裝 python 的 dependencies
```bash
pip install -r requirements.txt
```

3. 安裝 Tesseract。除了 python 對應的 Tesseract 模組之外，還得要安裝 Tesseract 引擎

For ubuntu/debian:
```bash
apt install -y tesseract-ocr
```
For FreeBSD:
```bash
pkg install -y tesseract
```

3. 使用指令介面或 API 介面
如果要使用指令介面請直接輸入
```bash
python ./parse.py [591 租屋網網址]
```

如果要使用 API 介面，請輸入
```bash
python ./app.py
```
打開瀏覽器輸入網址: http\://localhost:5000/591/[591 租屋網網址]

### 線上使用
https\://frankchang.me/591/\[591 租屋網網址\]

