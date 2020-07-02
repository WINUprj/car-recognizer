import io 
from io import BytesIO
import json
import re
import sys
import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import ImageMessage, MessageEvent, TextMessage, TextSendMessage
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from PIL import Image

from load import init

# directory to save images
IMAGE_DIR = './static/images'
if not os.path.isdir(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# direct path to images saved
IMAGE_PATH = './static/images/{}.jpg'

app = Flask(__name__)

# get access token and channel secret 
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

# create line bot api and webhook handler
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
web_handler = WebhookHandler(LINE_CHANNEL_SECRET)

header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN
}

model = init()

# simple check for server failures
@app.route('/')
def index():
    return 'hello world'

@app.route('/callback', methods=['POST'])
def callback():
    # get x-line-signature
    signature = request.headers['X-Line-Signature']
    # get request body as text 
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    try:
        web_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'Verified'

def reply_message(event, messages):
    # reply message from cnn model
    line_bot_api.reply_message(
        event.reply_token,
        messages=messages
    )

@web_handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    # get message id from image sent and add new path for it
    message_id = event.message.id 
    image_path = IMAGE_PATH.format(message_id)
    getImage(message_id, image_path)

    img_text = get_result(img_path=image_path)

    messages = [
        TextSendMessage(text=img_text)
    ]

    reply_message(event, messages)

def getImage(message_id, image_path):
    message_content = line_bot_api.get_message_content(message_id)
    with open(image_path, 'wb') as img:
        for chunk in message_content.iter_content():
            img.write(chunk)

def get_result(img_path):

    img = imread(img_path)

    if img is None:
        print('Image not open')

    img = img[10:len(img)-10, :]
    img = resize(img, (224, 224))
    img = np.asarray(img) / 225.0
    img = np.expand_dims(img, axis=0)
    pred = predict(img)

    return pred

def predict(img_src):
    brand = ''
    # 'Lamborghini', 'Ferrari', 'Bugatti', 'Rolls Royce', 'McLaren'
    brand_name = ['Ferrari', 'Bugatti', 'Rolls Royce', 'McLaren', 'Lamborghini']
    global model

    # if model is unloaded, initialize the model
    if model is None:
        model = init()
    
    pred = model.predict(img_src)
    pred_ind = np.argmax(pred)
    brand = brand_name[pred_ind]

    return brand

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)