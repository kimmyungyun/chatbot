import requests
from decouple import config

token = config('TELEGRAM_BOT_TOEKN')

url = f'https://api.telegram.org/bot{token}/getUpdates'

print(url)

res = requests.get(url).json()
user_id = res['result'][0]['message']['from']['id']
print(user_id)

send_url = f'https://api.telegram.org/bot{token}/sendMessage'

send_text = input("보낼 메세지를 입력해주세요 : ")
send_url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={send_text}'

result = requests.get(send_url)

print(result.text)