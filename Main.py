import csv
import numpy as np
from sklearn import svm


def getBeaconsFromSQL():
    print()


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

            # print(sameID)
            if sameID is False:
                # transpose and push location 2d array
                rez = [[arr[j][i] for j in range(len(arr))] for i in range(len(arr[0]))]
                arrayoflocations.append(rez)
                # print(arrayoflocations)
                # and clear the current 2d array
                arr = []

                rowcount = 0

            temp = []
            firstcol = True

            for col in row:
                # print(col)
                if firstcol is True:
                    firstcol = False
                    continue
                else:
                    temp.append(int(col))
            arr.append(temp)

            rowcount += 1
            # print(rowcount)

    # print(arrayoflocations)

    # formatting of cvs above
    ###################################
    # calling SVM below

    X = []
    for i in arrayoflocations:
        id = 0
        for j in i:
            maxreading = max(j)
            if maxreading != -1000:
                X.append((id, maxreading))
            id += 1

    # print(X)

    X = [(1, -79), (2, -82), (3, -29)]
    # this seemingly works-> X = [(1, -79), (2, -82), (3, -29)]
    # X= beacons3loc1
    # location1
    # 106,79
    # beacon1
    # 43,88
    # beacon2
    # 68,88
    # beacon3
    # 103,74

    # euclidean dist1
    # 63.6396
    # euclidean dist2
    # 39.05125
    # euclidean dist3
    # 5.83095
    filename = "id_to_coords.csv"
    IDdictionary = {}
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        # skip header
        next(csvreader)
        for row in csvreader:
            IDdictionary[row[0]] = (row[1], row[2])

    y = [63.6396, 39.05125, 5.83095]

    regr = svm.SVR(kernel="rbf")

    regr.fit(X, y)

    # print("beacon1, location2... used for prediction: ")
    # print(arrayoflocations[1][0])
    arrr = [1, -78]
    print(regr.predict(np.array(arrr).reshape(1, -1)))


SVMprediction()
