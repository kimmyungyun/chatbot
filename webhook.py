from decouple import config

token = config('TELEGRAM_BOT_TOEKN')
url = f'https://api.telegram.org/bot{token}/setWebhook'
ngrok_url = 'https://tata77.pythonanywhere.com/telegram'

setwebhook_url = f"{url}?url={ngrok_url}"

print(setwebhook_url)
