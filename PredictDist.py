import csv
import json
import sys
import pickle
import numpy as np
from sklearn import svm

activeBeaconsCoords = []


def getBeaconLocCoords():
    with open("beacons.csv", 'r') as csvfile:
        # creating a csv reader object
        csvreader2 = csv.reader(csvfile)
        for row in csvreader2:
            # active beaocn coords is the list of all beacons, which contains a list with that beacon's [ID, (X,Y)]
            activeBeaconsCoords.append([int(row[0]), (int(row[3]), int(row[4]))])


with open(f'SVM.pkl', 'rb') as f:
    regr = pickle.load(f)


def PredictDist(x, y, rssi):
    coordtuple = (x, y)
    beaconrssi = rssi
    inputarray = []
    for activeBeacon in activeBeaconsCoords:

        if (activeBeacon[1] == coordtuple):
            ID = activeBeacon[0]
            inputarray.append([ID, beaconrssi])
            break

    return regr.predict(np.array(inputarray).reshape(1, -1))


# alternatively...
# index = activeBeaconsCoords[2:2].index(coordtuple)
# ID = activeBeaconsCoords[index]
# inputarray.append([ID, beaconrssi])


PredictDist(sys.argv[1], sys.argv[2], sys.argv[3])
