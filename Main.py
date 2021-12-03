#!/usr/local/bin/python3
import nltk
import sys

# input = sys.argv[1]
import pickle
import csv
import math

import numpy as np
from sklearn import svm

regr = svm.SVR(kernel="rbf")
# instead of dictionary... use array of beacon IDs
NonusedBeacons = []
activeBeaconsCoords = []
LocationCoords = []


def getBeaconLocCoords():
    with open("beacons.csv", 'r') as csvfile:
        # creating a csv reader object
        csvreader2 = csv.reader(csvfile)
        for row in csvreader2:
            activeBeaconsCoords.append([int(row[0]), int(row[3]), int(row[4])])


def getLocationCoords():
    with open("id_to_coords.csv", 'r') as csvfile:
        # creating a csv reader object

        csvreader3 = csv.reader(csvfile)
        next(csvreader3)
        for row in csvreader3:
            LocationCoords.append([int(row[0]), (int(row[1]), int(row[2]))])


def SVMprediction():
    getBeaconLocCoords()
    getLocationCoords()
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

    # Formatting of csv above
    ###################################
    # calling SVM below

    X = []
    y = []
    ReadingLocID = 0
    for i in arrayoflocations:
        BeaconLocID = 0
        # update Location ID
        for j in i:
            maxreading = max(j)
            if maxreading != -1000:
                #if BeaconLocID == 2:
                    X.append((BeaconLocID, maxreading))
                   # print(ReadingLocID, BeaconLocID,  maxreading)
                    euclideandist = math.dist([LocationCoords[ReadingLocID][1][0], LocationCoords[ReadingLocID][1][1]],
                                              [
                                                  activeBeaconsCoords[BeaconLocID][1],
                                                  activeBeaconsCoords[BeaconLocID][2]])
                    y.append(euclideandist)
                   # print("euclidean dist:")
                    #print(euclideandist)
                    #print("x1 ")
                    #print(LocationCoords[ReadingLocID][1][0])
                    #print("y1 ")
                    #print(LocationCoords[ReadingLocID][1][1])
                    #print("x2 " )
                    #print(activeBeaconsCoords[BeaconLocID][1])
                    #print("y2 ")
                    #print(activeBeaconsCoords[BeaconLocID][2])

            BeaconLocID+=1

        ReadingLocID+= 1







    print(X)
    print(y)

    #print("location table")
    #print(LocationCoords)
    #print("beacons table")
    #print(activeBeaconsCoords)
    regr.C = 10000000000
    regr.gamma = 1
    regr.fit(X, y)

    print(regr.predict(np.array([1,-45]).reshape(1, -1)))


def SaveSVM(model):
    with open('SVM.pkl', 'wb') as file:
        pickle.dump(model, file)


SVMprediction()
SaveSVM(regr)
