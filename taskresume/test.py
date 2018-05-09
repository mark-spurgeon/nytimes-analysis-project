#!/usr/bin/env python
# -*- coding: utf-8 -*-
from taskresume import TaskBundle


#This is a test of how to use this task system

taskbundle = TaskBundle(slash_task=",\n")
#taskbundle.loadString('')
taskbundle.loadFile('test_tasks.txt')

if taskbundle.hasLoadedList:
    for task in taskbundle.list :
        args = task.get('args')
        status = task.get('status') # here, all tasks listed are not completed
        id = task.get('id')
        if args[0]=="https://google.com":
            taskbundle.changeStatus(id, 'error')
        else :
            taskbundle.changeStatus(id, 'yes')
