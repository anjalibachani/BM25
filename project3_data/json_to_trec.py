# -*- coding: utf-8 -*-


import json
# if you are using python 3, you should 
#import urllib.request 
import urllib.request
import string


# change the url according to your own corename and query
inurl = 'http://3.18.112.225:8983/solr/IRF20P3_BM25/select?defType=dismax&fl=id%2C%20score&q=Бильд.%20Внутренний%20документ%20говорит%2C%20что%20Германия%20примет%201%2C5%20млн%20беженцев%20в%20этом%20году&qf=text_en%20text_de%20text_ru&rows=20&wt=json'
outfn = '5.txt'

inurl=urllib.parse.quote(inurl,safe=string.printable)


# change query id and IRModel name accordingly
qid = '005'
IRModel='bm25' #either bm25 or vsm
outf = open(outfn, 'a+')
data = urllib.request.urlopen(inurl)
# if you're using python 3, you should use
# data = urllib.request.urlopen(inurl)

docs = json.load(data)['response']['docs']
# the ranking should start from 1 and increase
rank = 1
for doc in docs:
    outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
    rank += 1
outf.close()

