from flask import Flask, request
import requests
from rapidfuzz import fuzz

app = Flask(__name__)

BOT_TOKEN = "8103765408:AAFxvE-vmxcbx0AG8vo4_anSDPNAL7J4ncw"

# ✅ Step 1: Your smart knowledge base (dictionary)
WATER_TIPS = {
    "save water": "Turn off taps when not in use. Fix leaks. Use low-flow fixtures.",
    "reduce water usage": "Take shorter showers. Don't let water run while brushing teeth.",
    "reuse water": "Collect rainwater. Use leftover RO water for cleaning or gardening.",
    "importance of sanitation": "Good sanitation prevents disease and promotes hygiene.",
    "toilet hygiene": "Always flush. Keep the toilet clean. Wash hands with soap.",
    "conserve water": "Water plants early morning. Fix leaking taps and pipes.",
    "clean water": "Use water filters. Boil water before drinking. Avoid water pollution.",
}

# ✅ Step 2: Smart reply logic function
def smart_reply(user_message):
    best_score = 0
    best_reply = "Sorry, I didn’t understand that. Try asking about water saving or sanitation tips."

    for keyword, reply in WATER_TIPS.items():
        score = fuzz.ratio(user_message.lower(), keyword.lower())
        if score > best_score and score > 60:
            best_score = score
            best_reply = reply

    return best_reply

# ✅ Step 3: Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        reply = smart_reply(text)

        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(send_url, json={'chat_id': chat_id, 'text': reply})

    return 'ok'

# ✅ (Optional) Keep-alive route for Render/UptimeRobot
@app.route('/health')
def health():
    return "I'm alive!", 200
