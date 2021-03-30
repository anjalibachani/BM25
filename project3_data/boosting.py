import json
import urllib.request
from urllib.parse import quote

query_file = open('queries.txt', encoding="utf8")
queries = query_file.readlines()
query_id = ''
query_text = ''

IRModel = 'BM25'
outfn = 'boosting_query1_t5.txt'

boost_dict={
    'Russia\'s intervention in Syria':"",
    'US air dropped 50 tons of Ammo on Syria':"",
    'The European Refugee Crisis and Syria Explained animation':"",
    'Wegen Flüchtlingskrise: Angela Merkel stürzt in Umfragen':"",
    'РФ в Сирии вынудили 250 тунисских боевиков бежать':"",
    'ISIS Kills TOP Iranian General in Syria':"",
    'David Cameron urged to ensure vulnerable Syrian refugees are settled by winter':"",
    'RT @Free_Media_Hub':"",
    '#Hezbollah':"",
    '#Syria #SALMA #LATAKIA':"",
    'Greek AFP photojournalist Aris Messinis':"",
    'ASYL-FLÜCHTLING bedankt sich per Video-Botschaft bei Til Schweiger':"",
    'Airbnb, Instacart, Kickstarter launch campaigns to fund refugee relief':"",
    '12-year-old #Palestinian boy has died':"",
    'PM Medvedev’s delegation to coordinate anti-terrorist actions':""
}
    


def gallery_items(query):

    solr_tuples = [
       ('bq', boost_dict[query] ),
        ('q', query),
        ('rows', 20),
        ('start', 0),
        ('fl', 'id, score'),
        ('defType', 'edismax'),
        ('qf', 'text_en text_ru text_de'),
        ('wt', 'json')
    ]

    if boost_dict[query]=="":
        solr_tuples=solr_tuples[1:]

    return solr_tuples

for q in queries:
    print(q)
    query_id, query_text = map(str, q.strip().split(" ", 1))
    #query_text = query_text.replace(":", "\:")
    #query_text = quote(query_text)

    solr_tuples = gallery_items(query_text)
    solr_url = 'http://3.15.172.121:8983/solr/IRF20P3_BM25/select?'
    encoded_solr_tuples = urllib.parse.urlencode(solr_tuples)
    complete_url = solr_url + encoded_solr_tuples

    print(complete_url)

    outf = open(outfn, 'a+')
    data = urllib.request.urlopen(complete_url)
    docs = json.load(data)['response']['docs']

    # the ranking should start from 1 and increase
    rank = 1
    for doc in docs:
        outf.write(
            query_id + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(
                doc['score']) + ' ' + IRModel + '\n')
        rank += 1
    outf.close()

