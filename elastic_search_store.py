from elasticsearch import Elasticsearch
import urllib.request, json 
import ssl

es = Elasticsearch()

context = ssl._create_unverified_context()


with urllib.request.urlopen("https://api.myjson.com/bins/1bgkqj",context=context) as url:
    data = json.loads(url.read().decode())
    ##res = es.index(index="index", doc_type='teyit', id=id, body=data)
   
id=1 
for claim in data["claims"]:
    #print(claim)
    res = es.index(index="index", doc_type='teyit', id=id, body=claim)
    id+=1
    
    
es.indices.refresh(index="index")

res = es.search(index="index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
