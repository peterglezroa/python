import os
import csv
import random
import pandas
file = "model/model.csv"
def getModel(size):
    model = []
    print("Searchin last model....")
    if(os.path.isfile(file)):
        fil = pandas.read_csv(file)
        model = fil.values[len(fil.values) - 1]
    else:
        print("No prev model. Creating new one....")
        for i in range(size):
            model.append(0)
    return model

#Creates file and adds model
def createModelFile(params):
    print("Creating file; Saving model ", params, "....")
    params_names = []
    for i in range(len(params)):
        params_names.append('"Parameter %i"' % (i))
    with open(file, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(params_names)
        filewriter.writerow(params)

def appendModel(params):
    print("Saving model ", params, "....")
    with open(file, 'a') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(params)

def addModel(params):
    folder = "model"
    if(os.path.isfile(file)):
        appendModel(params)
    else:
        if(os.path.isdir(folder)):
            createModelFile(params)
        else:
            try:
                print("Creating folder....")
                os.mkdir(folder)
            except OSError:
                print ("Creation of the directory %s failed" % folder)
            else:
                print ("Successfully created the directory %s " % folder)
                createModelFile(params)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
model = getModel(5)
print(model)
addModel(model)
