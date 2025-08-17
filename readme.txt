Line

#datawin00002@gmail.com
webAPI:
https://developers.line.biz/console/channel/2007800550/messaging-api
channel secret f4a12ee553e64864614985e4885fa0d6
Channel access token MEd9R/HUGWBqDwshn5YNQ20/gFYhN33gfYK4BsRLoHV8xVlwBmchnXNldz/hJvwxzWk1AVTXslaLpbfW3TY6FhNu+DJy8PKrqdQK8G2NxXdbr5ZNnYh2Wh9MRC6WDbA/gL7+p5o3mWKIELGW2zC4FwdB04t89/1O/w1cDnyilFU=



ngrok
token
30H8PlmdYx6MNOquTwaKkWYVvsC_5Ejw2Qg5zGFT2hsyPmF8D

start up: 

https://steam.oxxostudio.tw/category/python/example/ngrok.html
key in command under dos:
ngrok config add-authtoken 30H8PlmdYx6MNOquTwaKkWYVvsC_5Ejw2Qg5zGFT2hsyPmF8D
note: user datawin00002@gmail.com




1. 輸入 token 後，繼續使用命令，將本機環境的埠號 port 對應到 ngrok 公開網址 

ngrok http http://127.0.0.1:5000

完成後，就會看到終端機裡出現 ngrok 的公開網址 ( 每次重新輸入後，網址都會改變 )
(Forwarding                    https://f05d467a854d.ngrok-free.app -> http://127.0.0.1:5000)

2. test if connected
使用本機的 Python 編輯器，或開啟 Anaconda Jupyter，安裝 Flask 後，執行下方的程式碼，會開啟一個本機網頁服務，網址為 127.0.0.1:5000。

from flask import Flask

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    return f"<h1>hello {name}</h1>"

app.run()

打開瀏覽器，輸入 127.0.0.1:5000/oxxo，畫面中就會出現 hello oxxo 的文字，但這個網址只有本機瀏覽器能夠使用，外部無法使用。

由於 5000 的埠號已經和 ngrok 串接，所以輸入剛剛的 ngrok 公開網址( https://f05d467a854d.ngrok-free.app)，就會看到一模一樣的結果，而這個網址，不論在任何地方，都能正常讀取。


3.正式串接webhook
參考 LINE 官方所提供的 Python 開發文件：LINE Messaging API SDK for Python，輸入下方的程式碼，安裝 LINE BOT 函式庫。
pip install line-bot-sdk


3.1 start up ngrok
    key in command under dos:
    3.1.1 ngrok config add-authtoken 30H8PlmdYx6MNOquTwaKkWYVvsC_5Ejw2Qg5zGFT2hsyPmF8D (token)
    3.1.2 ngrok http http://127.0.0.1:5000
3.2 run below code and then build bot server on local 127.0.0.1

from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = '你的 LINE Channel access token'
        secret = '你的 LINE Channel secret'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            print(msg)                                       # 印出內容
            reply = msg
        else:
            reply = '你傳的不是文字呦～'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    app.run()


3.3 send conmand as "ngrok http http://127.0.0.1:5000" showed from 3.2, into  dos command window from 3.1
3.4 
    3.4.1 modify webhook on line developer platform, followed  forward address from 3.3
    3.4.2 line developer platform webAPI:https://developers.line.biz/console/channel/2007800550/messaging-api
3.5 testing as chat with bot_friend, check if response 
    3.5.1 create line bot , webAPI, will be redirected to Line offical account. after done , you can then create webAPI in developer platform






