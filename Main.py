import csv
import numpy
from sklearn import svm


def SVMprediction():
    filename = "outputForSVM.csv"
    rowcount = 0

    arrayoflocations = []
    arr = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # skip header
        next(csvreader)

        firstrow = True
        for row in csvreader:
            sameID = True
            if firstrow:
                NewLocID = row[0]
                LocID = row[0]
                firstrow = False


            else:
                NewLocID = row[0]

            if LocID != NewLocID:
                LocID = NewLocID
                sameID = False

            #print(sameID)
            if sameID is False:
                # transpose and push location 2d array
                rez = [[arr[j][i] for j in range(len(arr))] for i in range(len(arr[0]))]
                arrayoflocations.append(rez)
                #print(arrayoflocations)
                # and clear the current 2d array
                arr = []


                rowcount = 0

            temp = []
            firstcol = True

            for col in row:
                #print(col)
                if firstcol is True:
                    firstcol = False
                    continue
                else:
                    temp.append(int(col))
            arr.append(temp)




            rowcount += 1
            # print(rowcount)

    #print(arrayoflocations)


    #formatting of cvs above
    ###################################
    #calling SVM below

    print(arrayoflocations[0][0])
    print(arrayoflocations[0][1])
    print(arrayoflocations[0][2])

    beacons3loc1=[[1,arrayoflocations[0][0]],[2,arrayoflocations[0][1]],[3,arrayoflocations[0][2]]]
    X = beacons3loc1

    #location1
    #106,79
    #beacon1
    #43,88
    #beacon2
    #68,88
    #beacon3
    #103,74


    #euclidean dist1
    #63.6396
    #euclidean dist2
    #39.05125
    #euclidean dist3
    #5.83095


    y = [63.6396, 39.05125,5.83095]

    regr = svm.SVR()
    # add in kernel
    regr.fit(X, y)
    #print(regr.predict([[1, arrayoflocations[1][0]]]))

