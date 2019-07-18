from bs4 import BeautifulSoup
import json
import requests

mainPageUrl = "https://teyit.org/"

def parseClaim(f, u):
    r = requests.get(u)
    soup = BeautifulSoup(r.content, 'html.parser')
    # print soup.find("time")['datetime'], u # for debugging
    if soup.find("div", class_="iddia_title") is not None:
        f.write(
            json.dumps({ "date": soup.find("time")['datetime'], "title": soup.find("h1", class_="entry-title cb-entry-title cb-title").text, "text": soup.find("div", class_="iddia_text").text, "truth": soup.find("div", class_="iddia_title").text, "link": u }, ensure_ascii=False).encode('utf8'))
        f.write(", ")
    else:
        return None

def getArticles(u):
    articles = []
    r = requests.get(u)
    soup = BeautifulSoup(r.content, 'html.parser')
    if soup.find("aside") is not None:
        soup.aside.decompose()
    for article in soup.find_all("article"):
        articles.append(article.a['href'])
    return articles


f = open("claims.txt", "w")
f.write("{ \"claims\": [")

for i in range(1, 40):
    articles = getArticles(mainPageUrl+"/page/"+str(i))
    for article in articles:
        parseClaim(f, article)

f.write("]}")
f.close()