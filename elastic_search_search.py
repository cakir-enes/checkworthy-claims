from elasticsearch import Elasticsearch

es = Elasticsearch()

es.indices.refresh(index="index")

query="Polis, stokçulara göz açtırmıyor, Ankara-Sincan\'da ekmek arasına gizlenmiş çok sayıda Marul stoku ele geçirildi"

res= es.search(index='index',body={'query':{'match':{'text':query}}})
print (res['hits']['hits'])
print("Got %d Hits:" % res['hits']['total']['value'])
