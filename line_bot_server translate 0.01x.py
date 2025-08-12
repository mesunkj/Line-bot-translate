from flask import Flask, request
# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
# from translate_vi_chn import main_entry_sync
from translate_vi_chn import main_entry_sync

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = 'your_access_token_here'
        secret = 'your_secret_here'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            print(msg)                                       # 印出內容
            # msg = g_trans_example(msg)
            # msg = main_entry(msg)
            msg =  main_entry_sync(msg)
            reply = msg
        else:
            reply = '你傳的不是文字呦～'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
    except Exception as e:
        print(f'error caused by {e}, body: {body}')                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略
def g_trans_example(msg):
    dialogue_translations = {
    # 中文發言, 翻譯成越南語
    "大家好,今天我們來討論這道應用題:一個水池有兩個水管,甲管單獨注滿水池需要6小時,乙管單獨注滿水池需要9小時.如果兩管同時開放,注滿水池需要多長時間?": 
    "Xin chao moi nguoi, hom nay chung ta se thao luan ve bai toan ung dung nay: Mot be nuoc co hai ong dan, ong A mot minh bom day be mat 6 gio, ong B mot minh bom day be mat 9 gio. Neu ca hai ong cung mo, mat bao lau de bom day be?",
    
    # 越南語發言, 翻譯成中文
    "Thua thay, em khong hieu cau hoi nay lam. \"Don doc truoc nuoc be\" la gi a?": 
    "老师,我不太理解这个问题.\"单独注满水池\"是什么意思呢?",
    
    "你好!\"單獨注滿水池\"的意思是,如果只有甲管在工作,乙管是關閉的,那麼甲管需要6小時把水池裝滿.同樣,如果只有乙管,則需要9小時.":
    "Chào em! \"Do day be mot minh\" co nghia la neu chi co ong A hoat dong va ong B tat, thi ong A can 6 gio de do day be. Tuong tu, neu chi co ong B, se mat 9 gio.",
    
    "A, em hieu roi a. Vay co phai la tinh tong cong viec cua ca hai ong khong a?":
    "啊,我明白了.那是不是要計算兩個管子的總工作量呢?",
    
    "對的,你理解很棒!這類問題我們通常會把它轉化為「工作效率」來計算.你可以想想甲管每小時能完成水池的多少比例?乙管又是多少?":
    "Dung vay, em hieu rat tot! Loai bai toan nay chung ta thuong chuyen doi no thanh \"hieu suat cong viec\" de tinh toan. Em co the nghi xem ong A moi gio co the hoan thanh bao nhieu phan tram be? Con ong B thi sao?",
    
    "Ong A moi gio do day 1/6 ho, va ong B moi gio do day 1/9 ho. Em tinh duoc roi a!":
    "甲管每小時可以注滿水池的 1/6,乙管每小時可以注滿水池的 1/9.我已經算出來了!",
    
    "太棒了!那麼兩管同時工作,每小時能完成水池的多少比例呢?":
    "Tuyet voi! Vay neu ca hai ong cung hoat dong, moi gio se hoan thanh bao nhieu phan tram be?",
    
    "Ca hai ong cung lam thi moi gio se do day (1/6 + 1/9) = 5/18 ho. Vay mat bao nhieu thoi gian de do day ho a?":
    "兩管同時工作的話,每小時會注滿水池的 (1/6 + 1/9) = 5/18.那麼要多久才能注滿水池呢?",
    
    "很好!所以注滿水池需要的時間就是 1 除以 (5/18).計算一下是多少?":
    "Rat tot! Vay thoi gian can de do day be la 1 chia cho (5/18). Tinh xem la bao nhieu?",
    
    "Em tinh duoc la 18/5 gio, tuc la 3 gio 36 phut. Dung khong a, thay?":
    "我算出來是 18/5 小時,也就是 3 小時 36 分鐘.對嗎,老師?",
    
    "完全正確!恭喜你,小明!你掌握了這類問題的解法.":
    "Hoan toan chinh xac! Chuc mung em, Minh! Em da nam vung cach giai loai bai toan nay."
    }


    if(msg in dialogue_translations):
        return dialogue_translations[msg]
    else:
        return "抱歉,我還不會翻譯這句話.請問你想說什麼呢?"  # 如果沒有對應的翻譯，返回一個預設訊息
if __name__ == "__main__":
    app.run()