from flask import Flask, escape, request, render_template
from decouple import config
import requests
token = config('TELEGRAM_BOT_TOEKN')
url = f'https://api.telegram.org/bot{token}/'
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name', "World")
    return f"Hello, {escape(name)}!"

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    request.args.get('user_id')
    res = requests.get(url+'getUpdates').json()

    user_id = res['result'][0]['message']['from']['id']
    send_text = request.args.get('user_text')
    send_url = f'{url}sendMessage?chat_id={user_id}&text={send_text}'

    result = requests.get(send_url)

    return render_template('send.html')

@app.route(f'/telegram', methods=['POST'])
def telegram():
    return 'ok', 200

if __name__=='__main__':
    app.run(debug=True)