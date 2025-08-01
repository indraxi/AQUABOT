from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
import os

app = Flask(__name__)

# Load env vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
NLU_API_KEY = os.getenv("NLU_API_KEY")
NLU_URL = os.getenv("NLU_URL")

# Watson setup
authenticator = IAMAuthenticator(NLU_API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
nlu.set_service_url(NLU_URL)

# Knowledge base
WATER_TIPS = {
    "save water": "Turn off taps when not in use. Fix leaks. Use low-flow fixtures.",
    "reduce water usage": "Take shorter showers. Don’t let water run while brushing teeth.",
    "reuse water": "Collect rainwater. Use leftover RO water for cleaning or gardening.",
    "importance of sanitation": "Good sanitation prevents disease and promotes hygiene.",
    "toilet hygiene": "Always flush. Keep the toilet clean. Wash hands with soap.",
    "conserve water": "Water plants early morning. Fix leaking taps and pipes.",
    "clean water": "Use filters. Boil water before drinking. Avoid pollution.",
}

def smart_reply(message):
    try:
        response = nlu.analyze(
            text=message,
            features=Features(keywords=KeywordsOptions(limit=3))
        ).get_result()

        for kw in response.get('keywords', []):
            keyword = kw['text'].lower()
            for key in WATER_TIPS:
                if key in keyword:
                    return WATER_TIPS[key]
    except:
        pass

    return "Sorry, I didn't get that. Try asking about water saving or sanitation tips."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        reply = smart_reply(text)

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={'chat_id': chat_id, 'text': reply}
        )
    return 'ok'

@app.route('/health')
def health():
    return "I'm alive", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
