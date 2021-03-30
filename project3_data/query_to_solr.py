import json
import urllib.request
from urllib.parse import quote

query_file = open('queries.txt', encoding="utf8")
queries = query_file.readlines()
query_id = ''
query_text = ''

IRModel = 'vsm'
outfn = 'vsm_default_synonyms.txt'

for q in queries:
    print(q)
    query_id, query_text = map(str, q.strip().split(" ", 1))
    query_text = query_text.replace(":", "\:")
    query_text = quote(query_text)

    # print(query_id, query_text)
    inurl = 'http://3.15.172.121:8983/solr/IRF20P3_VSM/select?defType=dismax&fl=id%2Cscore&q=' + query_text + '&qf=text_en%20text_de%20text_ru&wt=json&indent=true&rows=20'
    #print(inurl)
    outf = open(outfn, 'a+')
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']

    # the ranking should start from 1 and increase
    rank = 1
    for doc in docs:
        outf.write(
            query_id + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(
                doc['score']) + ' ' + IRModel + '\n')
        rank += 1
    outf.close()
