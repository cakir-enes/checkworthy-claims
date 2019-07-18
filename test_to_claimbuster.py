# encoding: utf-8
from googletrans import Translator
import urllib3, json, requests
from pandas_ml import ConfusionMatrix
import sys
reload(sys)
sys.setdefaultencoding("utf8")

def prepare_results(file):
    http = urllib3.PoolManager()
    claimBusterAPI = "https://idir.uta.edu:443/factchecker/score_text/"
    # JSONURL = "https://api.myjson.com/bins/qnijh" # balanced
    JSONURL = "https://api.myjson.com/bins/7da99" # imbalanced
    translator = Translator()

    r = http.request('GET', JSONURL)
    data = json.loads(r.data)

    f = open(file, 'w')
    f.write("{ \"results\": [")
    for claim in data:
        text = claim["tweet"].replace('\n', '').strip()
        translation = translator.translate(text).text.encode("utf8")
        res = requests.get(claimBusterAPI + translation)
        if res.status_code != 200:
            print "status code: ", res.status_code
            continue
        scores = res.json()["results"]
        max_score = 0
        for score in scores:
            if score["score"] > max_score:
                max_score = score["score"]
        f = open(file, 'a')
        f.write(
            json.dumps({"text": text,
                        "translation": translation,
                        "labellingScore": claim["has_checkworthy_claim"],
                        "score": score["score"]
                        }, ensure_ascii=False).encode("utf8"))
        f.write(",\n ")
        f.close()

    f = open(file, 'a')
    f.write("]}")
    f.close()

def process_results(mode, file, thrshld):
    threshold = thrshld
    with open(file) as json_file:  
        data = json.load(json_file)
        accuracy = 0.0
        actual = []
        predicted = []
        for p in data['results']:
            labellingScore = int(p['labellingScore']) 
            score = float(p['score'])
            if labellingScore == 1 and score > threshold:
                accuracy = accuracy + 1
            elif labellingScore == 0 and score < threshold:
                accuracy = accuracy + 1
            if labellingScore == 1:
                actual.append(1)
            else:
                actual.append(0)
            if score > threshold:
                predicted.append(1)
            else:
                predicted.append(0)
    if mode is 1:
        cm = ConfusionMatrix(actual, predicted)
        cm.print_stats()
    return accuracy/len(data['results'])

def get_optimal_threshold(file):
    max = 0
    temp = 0
    opt = 0
    arr = []
    for i in range(100):
        temp = process_results(0, file, float(i)/100)
        if temp > max:
            opt = (float(i)/100) 
            max = temp
    print opt
    return opt

balance_opt = get_optimal_threshold('testResults.txt')
print process_results(1, 'testResults_test.txt', balance_opt)

imbalance_opt = get_optimal_threshold('testResults_test.txt')
print process_results(1, 'testResults.txt', imbalance_opt)