#
#
#
#
#
#               Stage 2 : filter the articles that are of interest
#                         and put them in a taskbundle
#                         Selection by keywords : Will include only articles on presidential
#                         elections, Hillary Clinton, and Donald Trump
#
#
#
#
#
#
##

#This selection is intentionnaly limited, in order to reduce the size of articles
selectionofkeywords = [
    "Presidential Elections (US)",
    "Clinton, Hillary Rodham",
    "Trump, Donald J"
    ]


import simplejson as json
import os
from io import StringIO


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

mainjson = {"type":"combination", "period":"march 2015 to march 2018","results":[]}
resultslist = []

for f in os.listdir("data/stage1/"):
    if f.endswith('.json'):
        pa = os.path.join("data/stage1/", f)
        file = open(pa, encoding="utf-8")
        njson = json.load(StringIO(file.read()))
        nlist = njson.get('response').get('docs')
        file.close()
        #Create selection of items
        newdictlist = []
        for i, art in enumerate(nlist) :
            keywords = [k.get('value') for k in art.get('keywords')]
            select = False

            for k in selectionofkeywords:
                if k in keywords and select == False :
                    select = True
                else :
                    select = False

            if select == True:
                if art.get('headline').get('kicker')!= None:
                    headline = art.get('headline').get('kicker') + " ; " + art.get('headline').get('main')
                else :
                    headline = art.get('headline').get('main')

                newarticle = {
                    "url":art.get('web_url'),
                    "id":art.get('_id'),
                    "section":art.get('section_name'),
                    "keywords":keywords,
                    "headline":headline,
                    "pud_date":art.get('pub_date'),
                    "doc_type":art.get('type_of_material'),
                 }
                newdictlist.append(newarticle)

        resultslist+=newdictlist

mainjson['results']=resultslist
print("Number of selected articles : ", len(resultslist))


stage2_json = open('data/stage2/articles.json', 'w')
jsonstr = json.dumps(mainjson, indent=2, sort_keys=True)
stage2_json.write(jsonstr)
stage2_json.close()


notify("Finished task", "{} articles have been selected".format(len(resultslist)))

# create a task bundle
from taskresume.taskresume import TaskBundle

taskbundle = TaskBundle()
taskbundle.createFile('tasks/stage2.txt')

for res in resultslist:
    args = [
    res.get('id'),
    res.get('url')
    ]
    taskbundle.addTask({'args':args, 'status':'no'})

taskbundle.saveFile()

notify("Created a task taskbundle", "{} tasks to complete".format(len(resultslist)))
