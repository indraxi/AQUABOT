import os
import requests
from flask import Flask, request
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions

app = Flask(__name__)

# Load environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
IBM_API_KEY = os.environ.get("IBM_API_KEY")
IBM_NLU_URL = os.environ.get("IBM_NLU_URL")

# Watson NLU setup
authenticator = IAMAuthenticator(IBM_API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
nlu.set_service_url(IBM_NLU_URL)

# Static water-saving tips
WATER_TIPS = {
    'water': 'Turn off taps while brushing and fix leaks immediately.',
    'leak': 'Fix leaking pipes and toilets to conserve water.',
    'rain': 'Harvest rainwater using rooftop systems.',
    'toilet': 'Use dual-flush toilets to save water.',
    'laundry': 'Run full loads in your washing machine.'
}

def smart_reply(message):
    print("Analyzing with NLU:", message)
    try:
        response = nlu.analyze(
            text=message,
            features=Features(keywords=KeywordsOptions(limit=3))
        ).get_result()
        print("NLU Response:", response)

        for kw in response.get('keywords', []):
            keyword = kw['text'].lower()
            for key in WATER_TIPS:
                if key in keyword:
                    return WATER_TIPS[key]
    except Exception as e:
        print("NLU Error:", str(e))

    return "Sorry, I didn't get that. Try asking about water saving or sanitation tips."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received data:", data)

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        reply = smart_reply(text)

        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={'chat_id': chat_id, 'text': reply}
        )
        print("Telegram response:", response.text)
    return 'ok'

@app.route('/health')
def health():
    return "I'm alive", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

