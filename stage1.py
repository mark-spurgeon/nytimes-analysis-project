#
#
#
#
#               Stage 1 : Retrieve data for all periods defined in Stage 0
#
#
#
#
#
#
#  Other nytimes API urls
#  article search : https://api.nytimes.com/svc/search/v2/articlesearch.json
#  comments by url : http://api.nytimes.com/svc/community/v3/user-content/url.json
#
from credentials import nytimes_api_key
from taskresume.taskresume import TaskBundle
import requests
import json

import time
#TEST DOWN BELOW

taskbundle = TaskBundle(slash_task=",\n")
taskbundle.loadFile('TaskGroups/stage1.txt')

if taskbundle.hasLoadedList:
    for task in taskbundle.list:
        args = task.get('args')
        id = task.get('id')

        #notify which url is being treated
        print("Requesting url : ", args[0])


        parameters = {"api-key":nytimes_api_key}
        r = requests.get(args[0], params = parameters)
        try :
            if r.json():
                data = r.json()
            else :
                data = None

            if data:
                newdat = []
                jsonData = json.dumps(data, indent=4, sort_keys=True)
                file = open("data/stage1/{}.json".format(args[1]),"w")
                file.write(jsonData)
                file.close()
                taskbundle.changeStatus(id, 'yes')
                time.sleep(.300)
            else:
                taskbundle.changeStatus(id, 'error')
        except :
            taskbundle.changeStatus(id, 'error')
            file = open("data/stage1/{}.txt".format(args[1]),"w")
            file.write(r.text)
            file.close()
