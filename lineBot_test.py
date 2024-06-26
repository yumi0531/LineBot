from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# flask才會知道你的root在何處
app = Flask(__name__)

# 定義了一個 POST 請求的路由 /，這個路由將會接收 LINE Bot 的 webhook 訊息
# @app.route()裝飾器是 Flask 框架提供的功能，用來將 URL 路由和處理函式綁定在一起。
# "/" 是路由的路徑，表示這個路由會處理發送到根路徑（例如 http://example.com/）的 HTTP 請求。
@app.route("/", methods=['POST'])



# 處理 webhook 訊息
def linebot():
    body = request.get_data(as_text=True)  # 處取收到的 POST 訊息

    try:
        json_data = json.loads(body)  # json 格式化訊息內容

        access_token = 'eF5m9KLsF9RwhVVbgYy9452JYRO2kSu4fWUmZo+M5nTHoLzLHjbm2rm8J71FeJ7t7VHU1XxLTpydPXfVA7Vh1vJfhXoKzrQFHkz+Zz4F1aH6N4+uAIK//JeV/CDU0aImu1vjUQXDkS0hCzYDYSy9GAdB04t89/1O/w1cDnyilFU='
        secret = '0ff7498614217a843af7af35e8b86350'

        line_bot_api = LineBotApi(access_token) # 確認 token 是否正確
        handler = WebhookHandler(secret) # 確認 secret 是否正確

        signature = request.headers['X-Line-Signature'] 
        # X-Line-Signature 是 LINE 平台用來確認 webhook 訊息來源是否為正確的 LINE Bot 的一種安全機制。當 LINE Bot 收到來自 LINE 平台的 webhook 訊息時，會包含一個簽名（即 X-Line-Signature），用於確認訊息的真實性和完整性。這行程式碼確保你的應用能夠從 request 中取得這個簽名值，以便後續的驗證。

        handler.handle(body, signature)
        
        # 取得回傳訊息的 Token 和訊息類型
        tk = json_data['events'][0]['replyToken']
        type = json_data['events'][0]['message']['type']
        
        # 根據訊息類型處理訊息
        if type == 'text':
            msg = json_data['events'][0]['message']['text']
            print(msg)
            reply = msg
        else:
            reply = '你傳的不是文字呦～'
        print(reply)
        
        # 回傳訊息給 LINE 使用者
        line_bot_api.reply_message(tk, TextSendMessage(reply))
    except:
        print(body)
    
    return 'OK'
