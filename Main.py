import csv
from sklearn import svm


def SVMprediction():
    sameID = True
    LocID = 0
    NewLocID = 0
    filename = "outputForSVM.csv"
    rowcount = 0
    colcount = 0
    # amount of columns in csv
    cols = 34
    rows = 2168
    arrayoflocations = []
    arr = [[0 for i in range(cols)] for j in range(rows)]

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # skip header
        next(csvreader)

        for row in csvreader:
            sameID = True
            firstcol = True

            if LocID != NewLocID:
                LocID = NewLocID
                sameID = False

            if sameID is False:
                # push 2d array to an array,
                arrayoflocations.append(arr)
                print(arr)
                # and clear the current 2d array
                arr = [[0 for i in range(cols)] for j in range(rows)]
                # reset row iterator
                rowcount = 0

            # reset column iterator
            colcount = 0
            for col in row:
                if firstcol is True:
                    NewLocID = col
                    firstcol = False
                else:
                    # make a 2d array that will contain the rssi readings
                    #print(int(col))
                    arr[rowcount][colcount] = col
                    # it is supposed to be [rowcount] [colcount]

                colcount += 1

            rowcount += 1

    print(arrayoflocations)


# X = [[0, 0], [2, 2]]

# multi-label
# beacon coords
# y = [0.5, 2.5]

# regr = svm.SVR()
# add in kernel
# regr.fit(X, y)
# regr.predict([[1, 1]])
SVMprediction()
