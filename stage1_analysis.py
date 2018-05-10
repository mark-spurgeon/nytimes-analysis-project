#
#
#
#
#
#
#               Stage 1 bis : analysis of the retrieved data
#
#
#
#
#
##

import simplejson as json
import pandas
import os
from io import StringIO

mainjson = {"type":"combination", "period":"march2015-march2018","results":[]}
resultslist = []

for f in os.listdir("data/stage1/"):
    if f.endswith('.json'):
        pa = os.path.join("data/stage1/", f)
        file = open(pa, encoding="utf-8")
        njson = json.load(StringIO(file.read()))
        nlist = njson.get('response').get('docs')
        file.close()
        resultslist+=nlist

mainjson['results']=resultslist
print("Number of articles : ", len(resultslist))


# Analysis - sections
####
sectionslist = []
sections = {}

for r in mainjson.get('results'):
    sectionname = str(r.get('section_name'))
    if sectionname in sectionslist:
        sections[sectionname]+=1
    else :
        sectionslist.append(sectionname)
        sections[sectionname] = 1
ana1 = open('analysis/sections.json', 'w')
ana1.write(json.dumps(sections, indent=2, sort_keys=True))
ana1.close()
print('done with sections')


# Analysis - keywords
####
keywordslist = []
keywords = {}

for r in mainjson.get('results'):
    keywo = r.get('keywords')
    for k in keywo:
        word = k.get('value')
        if word in keywordslist:
            keywords[word]+=1
        else :
            keywordslist.append(word)
            keywords[word] = 1
ana2 = open('analysis/keywords.json', 'w')
jsonstr = json.dumps(keywords, indent=2, sort_keys=True)
ana2.write(jsonstr)
ana2.close()
print('done with keywords')
