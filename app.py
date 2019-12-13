from flask import Flask, escape, request, render_template
from decouple import config
import requests
import random

token = config('TELEGRAM_BOT_TOEKN')
google_key = config('GOOGLE_KEY')
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
    req = request.get_json()
    user_id = req['message']['chat']['id']
    user_input = req['message']['text']


    if user_input == '로또':
        return_data = "로또를 입력하셨습니다."

        lotto_num = random.choices(list(range(1,46)), k=6)
        print(lotto_num)
        lotto_string = ""
        for i in sorted(lotto_num):
            lotto_string += (str(i) + " ")
        send_url = f"{url}sendMessage?chat_id={user_id}&text={lotto_string}"
        requests.get(send_url)

    elif user_input[0:2] == "번역":
        before_text = user_input[3:-1]
        translation_url = f"https://translation.googleapis.com/language/translate/v2"

        data = {
            'q':before_text,
            'source':'ko',
            'target':'en',
        }
        requests_url = f'{translation_url}?key={google_key}'
        res = requests.post(url=requests_url, data=data).json()
        print(res)
        return_data = "번역기능을 실험합니다."
        after_text = res['data']['translations'][0]['translatedText'].replace('&#39;', "'")
        send_url = f"{url}sendMessage?chat_id={user_id}&text={after_text}"
        requests.get(send_url)
    else:
        return_data = "지금 사용 가능한 명령어는 로또입니다."
        send_url = f'{url}sendMessage?chat_id={user_id}&text={return_data}'
        requests.get(send_url)

    # print(return_data)
    print(f'{user_id} 님이 {return_data}이라는 문자를 보내셨습니다')


    return 'ok', 200

if __name__=='__main__':
    app.run(debug=True)