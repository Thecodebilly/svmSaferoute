import pickle
import csv
import math
import numpy
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# instead of dictionary... use array of beacon IDs
NonusedBeacons = []
activeBeaconsCoords = []
LocationCoords = []
X = []
y = []


# R^2 method to quantify the model's accuracy, adjusts for overfitting
def AdjustedRSquared(RSquared, n, k):
    return 1 - ((1 - RSquared) * (n - 1) / (n - k - 1))


# gets the beacon coordinates for the Beacons table in the myPHPAdmin
def getBeaconLocCoords():
    with open("beacons.csv", 'r') as csvfile:
        # creating a csv reader object
        csvreader2 = csv.reader(csvfile)
        for row in csvreader2:
            activeBeaconsCoords.append([int(row[0]), int(row[3]), int(row[4])])


# gets the location coordinates from the Java data cleaner file
def getLocationCoords():
    with open("id_to_coords.csv", 'r') as csvfile:
        # creating a csv reader object

        csvreader3 = csv.reader(csvfile)
        next(csvreader3)
        for row in csvreader3:
            LocationCoords.append([int(row[0]), (int(row[1]), int(row[2]))])


def SaveSVM(model):
    with open('SVM.pkl', 'wb') as file:
        pickle.dump(model, file)


# populates the dependent and independent variables to be input into the SVM
def SVMprediction():
    getBeaconLocCoords()
    getLocationCoords()
    filename = "outputForSVM.csv"
    rowcount = 0

    arrayoflocations = []
    arr = []

    # reading main output from Java cleaner (outputForSVM)
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # skip header
        next(csvreader)

        # getting first Location ID
        firstrow = True
        for row in csvreader:
            sameID = True
            if firstrow:
                NewLocID = row[0]
                LocID = row[0]
                firstrow = False

            # record Location ID for current row
            else:
                NewLocID = row[0]
            # if the location ID changed from last row, flag that the ID has changed
            if LocID != NewLocID:
                LocID = NewLocID
                sameID = False

            # act on flag, store all data for this location ID
            if sameID is False:
                # transpose and push location 2d array
                # this is to store all the columns of data for a given beacon at a location in an array
                # each row contains all of the readings for a beacon at a location ID
                rez = [[arr[j][i] for j in range(len(arr))] for i in range(len(arr[0]))]
                arrayoflocations.append(rez)
                # and clear the current 2d array
                arr = []

                rowcount = 0

            # temp is to store RSSIs
            temp = []

            firstcol = True

            for col in row:
                # now we are getting RSSI readings from each row, so skip the first index (the location ID)
                if firstcol is True:
                    firstcol = False
                    continue
                else:
                    # append the RSSI as an int
                    temp.append(int(col))
            # append the row of RSSIs for the current row in the current location ID to the array for the whole location ID
            arr.append(temp)

            # ++1
            rowcount += 1

    # Formatting of csv above
    ###################################
    # calling SVM below

    ReadingLocID = 0
    # for the column of data in a given location for a beacon
    for i in arrayoflocations:
        BeaconLocID = 0
        # update Location ID
        # for value in data column
        for j in i:
            # get best RSSI in data column (because highest RSSI is most accurate)
            maxreading = max(j)
            # if not placeholder value
            if maxreading != -1000:
                # add dependant variable
                X.append((BeaconLocID, maxreading))

                # add independent value
                euclideandist = math.dist([LocationCoords[ReadingLocID][1][0], LocationCoords[ReadingLocID][1][1]],
                                          [
                                              activeBeaconsCoords[BeaconLocID][1],
                                              activeBeaconsCoords[BeaconLocID][2]])
                y.append(euclideandist)

                # we are using the tuple of (BeaconLocID, maxreading) to predict the distance
                # from a beacon to a user who got the RSSI reading

            BeaconLocID += 1

        ReadingLocID += 1


# get X,y
SVMprediction()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.001, random_state=1)

algArr = []
n = 2.25
for xval in X_test:
    exp = (-65 - xval[1]) / (10 * n)
    dist = 3.28 * math.pow(10, exp)
    algArr.append(dist)

c = 1
rmse_svm = []
y_true = y_test
for i in range(5):
    regr = svm.SVR(kernel="rbf")
    regr.C = c
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)
    print(regr.score(X_test, y_test))
    print(AdjustedRSquared(regr.score(X_test, y_test), len(X_train), 34))
    rmse_svm.append(math.sqrt(mean_squared_error(y_true, y_pred)))
    c = c * 10

rmse_alg = math.sqrt(mean_squared_error(y_true, algArr))

# penalty

# regr.gamma =1

# regr.degree

# regr.coef0

# formulaic/algorithmic approach ( for comparison )


# print(sum(abs(numpy.subtract(numpy.array(y_true), numpy.array(y_pred)))))


print(rmse_svm)
# SaveSVM(regr)

data = {'SVM, C=1': rmse_svm[0], 'SVM, C=10': rmse_svm[1], 'SVM, C=100': rmse_svm[2], 'SVM, C=1000': rmse_svm[3],
        'SVM, C=10000': rmse_svm[4], 'formula': rmse_alg}
courses = list(data.keys())
values = list(data.values())

fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.bar(courses, values, color='maroon',
        width=0.4)

plt.xlabel("Model Used")
plt.ylabel("Root Mean Squared Error (RMSE)")
plt.title("RMSE of RSSI-to-Distance Methods")
plt.show()
