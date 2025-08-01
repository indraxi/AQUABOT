import requests

BOT_TOKEN = '8103765408:AAFxvE-vmxcbx0AG8vo4_anSDPNAL7J4ncw'
NGROK_URL = 'https://8a34a55f3cbe.ngrok-free.app'

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
payload = {"url": f"{NGROK_URL}/webhook"}

response = requests.post(url, data=payload)
print(response.text)