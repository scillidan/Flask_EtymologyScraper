from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)
CORS(app)

def get_oldest_etymology(word):
    url = f"https://www.etymonline.com/word/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Origin not found"

    soup = BeautifulSoup(response.text, "html.parser")


    etymology_section = soup.find("section", class_="word__defination--2q7ZH")

    if etymology_section:
        full_etymology = etymology_section.get_text(strip=True)

        proto_germanic_search = re.search(r'(from Proto-Germanic)', full_etymology, re.IGNORECASE)
        if proto_germanic_search:
            return f"{proto_germanic_search.group(1)}"

        oldest_match = re.search(r'(from (Latin|Greek|Sanskrit|Old Norse|German|Proto-Italic|Old Norse|Old High German|Old French|Mandarin))', full_etymology, re.IGNORECASE)
        if oldest_match:
            return f"{oldest_match.group(0)}"

        second_oldest_match = re.search(r'(Latin|Greek|Sanskrit|Old Norse|Proto-Germanic|German|Proto-Italic|Old Norse|Old High German|Old French|Old English|Irish|Japanese|American English)',full_etymology, re.IGNORECASE)
        if second_oldest_match:
            return f"{second_oldest_match.group(1)}"

        return full_etymology

    return "No etymology found for this word."

@app.route('/org', methods=['GET'])
def word_origin():
    word = request.args.get("word", "").strip().lower()
    if not word:
        return jsonify({"error": "Please provide a word."}), 400

    origin = get_oldest_etymology(word)
    return jsonify({"word": word, "oldest_origin": origin})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)