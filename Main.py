import csv
from sklearn import svm


def SVMprediction():
    filename = "outputForSVM.csv"
    rowcount = 0
    colcount = 0

    # amount of columns in csv
    cols = 100

    arrayoflocations = []
    arr = [[] for i in range(cols)]

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # skip header
        next(csvreader)

        firstrow = True
        for row in csvreader:
            sameID = True
            #print(row)
            #print("again")
            if firstrow:
                #print(row[0])
                NewLocID = row[0]
                LocID= row[0]
                firstrow=False


            else:
                NewLocID= row[0]
           #print("new")
           # print(NewLocID)
            #print("old")
            #print(LocID)
            if LocID != NewLocID:
                LocID = NewLocID
                sameID = False

            #print(sameID)
            if sameID is False:
                #print(arr)
                # push 2d array to an array,
                # print(arr)
                arrayoflocations.append(arr)

                # and clear the current 2d array

                arr = [[] for i in range(cols)]
                #print(arr)

                #print(arr)
               #print("\n\nin")

                # reset row iterator
                rowcount = 0

            # reset column iterator
            colcount = 0
            firstcol=True
            for col in row:
                #print(col)
                if firstcol is True:
                    firstcol=False
                    #NewLocID = col
                    #firstcol = False
                else:
                    # make a 2d array that will contain the rssi readings
                    # print(int(col))

                    arr[rowcount-1].append(int(col))

                colcount += 1
            #print(colcount)
            rowcount += 1
            #print(rowcount)


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
