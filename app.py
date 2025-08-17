from flask import Flask, render_template, request, jsonify
import json, re

app = Flask(__name__)

with open('faqs.json', 'r', encoding='utf-8') as fh:
    FAQS = json.load(fh)

def match_intent(text: str):
    t = text.lower().strip()
    for item in FAQS:
        for pattern in item.get("patterns", []):
            if re.search(pattern, t):
                return item["answer"]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json() or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({'reply':'Please type a question.'})
    ans = match_intent(message)
    if ans:
        return jsonify({'reply': ans})
    return jsonify({'reply': "I'm not sure about that. Try asking about projects, certificates, or deadlines."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
