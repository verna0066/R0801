from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from engine.currencySearch import currencySearch

app = Flask(__name__)

# 設定你的Channel Access Token
line_bot_api = LineBotApi('cwa3kAAZIPhwEfq0iDw52QDzGrvyyF0NhdkkJhoULNpLBYglNrQ9KuZu3Hr/KjKTw5PkAYYiuboTRVDxM417+SNfUrkCmx5NNv52uzADNr1od+TubTiTFc/veNwhoTTnANEFv2J9TwkUKa6StI0PtQdB04t89/1O/w1cDnyilFU=')
# 設定你的Channel Secret
handler = WebhookHandler('b52daf95693b1ced5d0e9448284150eb')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'
@app.route('/web')
def showeb():
	return '<h1> HELLO EVERY ONE</h1>'
#處理訊息
#當訊息種類為TextMessage時，從event中取出訊息內容，藉由TextSendMessage()包裝成符合格式的物件，並貼上message的標籤方便之後取用。
#接著透過LineBotApi物件中reply_message()方法，回傳相同的訊息內容
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	userSend = event.message.text
	userID = event.source.user_id

	if userSend == "你好":
		message = TextSendMessage(text='HELLO, '+userID)
	elif userSend == "再見":
		message = StickerSendMessage(package_id='11539',sticker_id='52114110')
	elif userSend == "美金":
		message = TextSendMessage(text=currencySearch('USD'))
	elif userSend == "日幣":
		message = TextSendMessage(text=currencySearch('JPY'))
	elif userSend in ['CNY', 'THB', 'SEK', 'USD', 'IDR', 'AUD', 'NZD', 'PHP', 'MYR', 'GBP', 'ZAR', 'CHF', 'VND', 'EUR', 'KRW', 'SGD', 'JPY', 'CAD', 'HKD']
		message = TextSendMessage(text=currencySearch(userSend))
	else :
		message = TextSendMessage(text=userSend)
	line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
	message = TextSendMessage(text='我看不懂貼圖')
	line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
