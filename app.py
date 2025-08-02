from flask import Flask, request
import requests
import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
NLU_API_KEY = os.getenv("NLU_API_KEY")
NLU_URL = os.getenv("NLU_URL")

authenticator = IAMAuthenticator(NLU_API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
nlu.set_service_url(NLU_URL)

WATER_TIPS = {
    "leak": "Fix leaking taps and pipes to save water.",
    "toilet": "Use dual flush toilets to reduce water use.",
    "shower": "Take shorter showers to conserve water.",
    "sanitation": "Ensure proper sanitation to avoid waterborne diseases."
}

def smart_reply(message):
    try:
        response = nlu.analyze(
            text=message,
            features=Features(keywords=KeywordsOptions(limit=3))
        ).get_result()

        print(f"NLU response: {response}")  # Log NLU analysis result

        for kw in response.get('keywords', []):
            keyword = kw['text'].lower()

            print(f"Detected keyword: {keyword}")  # Log keyword

            for key in WATER_TIPS:
                if key in keyword:
                    return WATER_TIPS[key]
    except Exception as e:
        print(f"NLU Error: {e}")  # Log error if any

    return "Sorry, I didn't get that. Try asking about water saving or sanitation tips."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        print("📩 Incoming message:", text)  # <-- LOG HERE

        reply = smart_reply(text)

        print("💬 Replying with:", reply)     # <-- LOG HERE

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={'chat_id': chat_id, 'text': reply}
        )
    return 'ok'

@app.route('/health')
def health():
    return "I'm alive", 200

