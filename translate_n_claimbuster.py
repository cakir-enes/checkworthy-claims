# encoding: utf-8
from googletrans import Translator
import requests, json
import sys
reload(sys)
sys.setdefaultencoding("utf8")

claimBusterAPI = "https://idir.uta.edu:443/factchecker/score_text/"
JSONURL = "https://api.myjson.com/bins/1bgkqj"
translator = Translator()

data = json.loads(requests.get(JSONURL).content)
f = open("output.txt", 'w')
f.write("{ \"claims\": [")

for claim in data["claims"]:
    text = claim["text"][claim["text"].find(':') + 2:].replace('\n', '').strip()
    translation = translator.translate(text).text.encode("utf8")
    scores = requests.get(claimBusterAPI + translation).json()["results"]
    max_score = 0
    for score in scores:
        if score["score"] > max_score:
            max_score = score
    f.write(
        json.dumps({"text": text,
                    "translation": translation,
                    "score": score
                    }, ensure_ascii=False).encode("utf8"))
    f.write(", ")

f.write("]}")
f.close()
