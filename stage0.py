##
#
#
#
#
#                   Stage 0 : set up all the months where we will need data
#                   from : march 2015 (start of campaigns)
#                   elections : november 2016
#                   to : march 2018 (can do with earlier)
#
#
#
#
#
##

from taskresume.taskresume import TaskBundle

taskbundle = TaskBundle()
taskbundle.createFile('tasks/stage1.txt')

base_url = "https://api.nytimes.com/svc/archive/v1/{0}/{1}.json" #where 0 is the year, 1 is the month
year_list = [2015, 2016, 2017, 2018]
month_list = range(13) # march : 3


all_urls = []



for year in year_list :
    for month in month_list:
        calc = True
        if year==2015 and month<=2 :
            calc = False
        if year==2018 and month>=4 :
            calc = False
        if month==0:
            calc = False

        if calc==True:
            all_urls.append({
                "url":base_url.format(year,month),
                "id":str(year)+"-"+str(month)
                })

for u in all_urls:
    taskbundle.addTask({"args":[u.get('url')], "status":"no"})

taskbundle.saveFile()
