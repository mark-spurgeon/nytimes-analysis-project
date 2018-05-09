
class TaskBundle :
    def __init__(self, slash_arg=" ", slash_task=";\n", status_no="--", status_yes= "OK", status_error= "ERROR"):
        self.slash_arg = slash_arg
        self.slash_task = slash_task
        self.status_no = status_no
        self.status_yes = status_yes
        self.status_error = status_error

        # global variables that are calculated by functions
        self.wholelist = []
        self.list = []

        #state
        self.hasLoadedList = False

        #string settings
        self.outputstring = ""
        #file settings
        self.usefile = False
        self.fileobject = None
        self.filename=""


    def _updateString(self):
        stringue = ""
        for task in self.wholelist:
            for arg in task.get('args'):
                stringue+=arg
                stringue+=self.slash_arg
            stringue+=task.get('status')
            stringue+=self.slash_task
        if stringue!="":
            self.outputstring=stringue
            return stringue
        else :
            return None
    def _selectList(self):
        if self.wholelist:
            taskstocomplete = []
            for task in self.wholelist:
                status = task.get('status')
                if status == self.status_no :
                    taskstocomplete.append(task)
            self.list = taskstocomplete
            return self.list
        else :
            return None


    def _setWholeListFromString(self, stringue):
        listofunparsedtasks = stringue.split(self.slash_task)
        if len(listofunparsedtasks)==0:
            print("No item, there must be an error in your file or in the settings you set to your TaskBundle")
            return None
        else :
            listofformattedtasks = []
            for i, unparsedtask in enumerate(listofunparsedtasks):
                if unparsedtask=="" :
                    print("INFO : line {} had nothing in it".format(i))
                else :
                    listofitems = unparsedtask.split(self.slash_arg);
                    status = listofitems[-1:][0]
                    args = listofitems[:-1]

                    item = {"args" : args, "status":status, "id":i}
                    listofformattedtasks.append(item)

            self.wholelist=listofformattedtasks
            return listofformattedtasks


    def changeStatus(self, id, status):
        newtasks = []
        for task in self.wholelist:
            if task.get('id')== id:
                if status=="error":
                    task['status']=self.status_error
                elif status=="yes":
                    task['status']=self.status_yes
                elif status=="no":
                    task['status']=self.status_no
            newtasks.append(task)

        self.wholelist=newtasks
        self._selectList()
        self._updateString()

        if self.usefile:
            f = open(self.filename, "w")
            f.write(self.outputstring)
            f.close()




    def loadFile(self, filename):
        try :
            fileobject = open(filename)
            self.usefile = True
            self.filename=filename

            setWholeList = self._setWholeListFromString(fileobject.read())

            if setWholeList:
                setTaskList = self._selectList()
                if setTaskList:
                    self.hasLoadedList=True
                    return True
                else :
                    print("Error while setting up the list of tasks, might be a problem with formatting the status")
                    return False
            else:
                print("Error while setting up the list of tasks.")
                return False

        except :
            print ("File loading error : either the file doesn't exist or it is not permited to read and write to it.")
            return False
