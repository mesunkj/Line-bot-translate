# LineBot-VI-CHN-Translator

# **LINE Bot 翻譯機器人 操作手冊（詳細版）**

## **1\. 專案簡介**

本專案是一個 **LINE Bot**，支援 **繁體中文 ↔ 越南語** 的自動雙向翻譯，並可處理長文本。  
 技術上採用：

* **Flask** 作為後端 API Framework

* **LINE Messaging API** 進行訊息收發

* **Google Translate** 作為翻譯服務

* **ngrok** 提供本機伺服器的公開網址

應用場景：

* 語言教學

* 語言交流

* 跨文化溝通

---

## **2\. 系統架構**

使用者 ↔ LINE 平台 ↔ Flask API (Line Bot Server) ↔ Google Translate

* **ngrok**：將本機的 Flask 伺服器映射到公開網路

* **LINE Bot 平台**：註冊並管理 Bot

* **Flask**：提供 API 端點，處理訊息

* **Google Translate API**：處理文字翻譯

---

## **3\. 安裝與環境設定**

### **3.1 安裝 Python 與套件**

1. 建立虛擬環境（建議做法）

python \-m venv .venv  
source .venv/bin/activate   \# Linux/Mac  
.venv\\Scripts\\activate      \# Windows

2. 安裝依賴套件

pip install \-r requirements.txt

### **3.2 下載專案**

專案原始碼：  
 [GitHub \- mesunkj/Line-bot-translate](https://github.com/mesunkj/Line-bot-translate)

git clone https://github.com/mesunkj/Line-bot-translate.git  
cd Line-bot-translate

---

## **4\. ngrok 設定**

### **4.1 申請 token**

前往 [ngrok 官方網站](https://ngrok.com/) 申請帳號，取得 authtoken。  
 參考教學：[Oxxo Studio ngrok 教學](https://steam.oxxostudio.tw/category/python/example/ngrok.html)

### **4.2 設定 ngrok**

進入 ngrok 安裝目錄，執行以下指令：

ngrok config add-authtoken \<你的-authtoken\>

啟動對應本機 5000 port：

ngrok http http://127.0.0.1:5000

成功後，終端機會顯示 Forwarding 連結，例如：

Forwarding    https://c371f3687913.ngrok-free.app \-\> http://127.0.0.1:5000

⚠️ **注意**：每次重啟 ngrok，網址會改變。

---

## **5\. LINE Bot 設定**

### **5.1 建立 Messaging API Channel**

1. 登入 [LINE Developers Console](https://developers.line.biz/console/)

2. 建立 **Messaging API** Channel

3. 取得以下資訊：

   * **Channel Secret**

   * **Channel Access Token**

範例：  
 [LINE Developer Console Channel Example](https://developers.line.biz/console/channel/2007800550/messaging-api)

### **5.2 設定 Webhook**

將剛剛 ngrok 提供的網址（例如 `https://c371f3687913.ngrok-free.app`）填入 LINE Developer Console → Webhook URL。

---

## **6\. 啟動 Flask 伺服器**

### **6.1 執行專案**

修改專案程式，填入 `Channel Access Token` 與 `Channel Secret`，檔案位置：  
 `line_bot_server translate 0.01x.py`

然後啟動伺服器：

python "line\_bot\_server translate 0.01x.py"

### **6.2 測試 Flask**

最小範例（Hello World）：

from flask import Flask  
app \= Flask(\_\_name\_\_)

@app.route("/\<name\>")  
def home(name):  
    return f"\<h1\>Hello {name}\</h1\>"

app.run()

* 在瀏覽器輸入 `http://127.0.0.1:5000/oxxo` → 顯示 **Hello oxxo**

* 在外部瀏覽器輸入 ngrok 提供的網址 → 顯示相同結果

---

## **7\. LINE Bot 測試**

### **7.1 安裝 LINE SDK**

pip install line-bot-sdk

### **7.2 簡單測試程式**

from flask import Flask, request  
import json  
from linebot import LineBotApi, WebhookHandler  
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app \= Flask(\_\_name\_\_)

@app.route("/", methods=\['POST'\])  
def linebot():  
    body \= request.get\_data(as\_text=True)  
    json\_data \= json.loads(body)  
    access\_token \= '你的 LINE Channel access token'  
    secret \= '你的 LINE Channel secret'  
    line\_bot\_api \= LineBotApi(access\_token)  
    handler \= WebhookHandler(secret)

    tk \= json\_data\['events'\]\[0\]\['replyToken'\]  
    msg \= json\_data\['events'\]\[0\]\['message'\]\['text'\]  
    reply \= f"你傳來的訊息是：{msg}"  
    line\_bot\_api.reply\_message(tk, TextSendMessage(reply))  
    return 'OK'

if \_\_name\_\_ \== "\_\_main\_\_":  
    app.run()

---

## **8\. 測試與驗證**

1. 在 LINE App 上新增你建立的 Bot 為好友

2. 傳送訊息 → Bot 回覆相同文字（測試成功）

3. 測試翻譯功能（中文 ↔ 越南語）

---

## **9\. 參考連結總整理**

* Ngrok 教學：[Oxxo Studio](https://steam.oxxostudio.tw/category/python/example/ngrok.html)

* Ngrok 官網：[https://ngrok.com/](https://ngrok.com/)

* GitHub 專案：[Line-bot-translate](https://github.com/mesunkj/Line-bot-translate)

* LINE Developer Console：[https://developers.line.biz/console/](https://developers.line.biz/console/)

* 範例 Channel：[Messaging API Example](https://developers.line.biz/console/channel/2007800550/messaging-api)

* LINE Messaging API SDK for Python：[官方文件](https://github.com/line/line-bot-sdk-python)



## 主要檔案

- [`line_bot_server translate 0.01x.py`](line_bot_server%20translate%200.01x.py)：LINE Bot 主伺服器
- [`translate_vi_chn.py`](translate_vi_chn.py)：翻譯核心模組
- [`requirements.txt`](requirements.txt)：依賴套件清單

## 參考

- [LINE Messaging API 官方文件](https://developers.line.biz/console/channel/2007800550/messaging-api)
- [Googletrans](https://pypi.org/project/googletrans/)
- [ngrok](https://steam.oxxostudio.tw/category/python/example/ngrok.html)

---

如需協助或回報問題，請開啟 Issue。
