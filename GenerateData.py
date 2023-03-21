import os, sys, csv
import pandas as pd
import ShowGraph

def WriteData(filename, data, method):


    data = ConvertDates(data)
    data = ConvertKM(data)
    data = AvgPace(data)
    data = AvgSpeed(data)


    if method == "new":
        NewData(filename, data)

    else:
        AppendData(filename, data)


def NewData(filename, data):
    with open(os.path.join(sys.path[0], filename), mode="w", newline='') as csvfile:
        fieldnames = ["Date", "Distance KM", "Distance Miles", "Duration", "Avg Pace KM", "Avg Pace Miles", "Avg Speed KMH", "Avg Speed MPH"]
        print(data)
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for row in data:
            writer.writerow(row)
    ReadData(filename)



def AppendData(filename, data):
    with open(os.path.join(sys.path[0], filename), mode="a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)
    ReadData(filename)


def ReadData(filename):
    dataset = pd.read_csv(os.path.join(sys.path[0], filename), index_col=0)
    Dates = [str(_) for _ in dataset.index]
    print(Dates)
    newDates = []
    for i in range(len(Dates)):
        newDate = ""
        if len(Dates[i]) != 10:
            print("HI")
            if len(Dates[i].split('.')[0]) == 1:
                newDate += ("0" + Dates[i].split('.')[0] + "/")
            else:
                newDate += (Dates[i].split('.')[0] + "/")
            if len(Dates[i].split('.')[1]) == 1:
                newDate += ("0" + Dates[i].split('.')[1] + "/")
            else:
                newDate += (Dates[i].split('.')[1] + "/")
            if len(Dates[i].split('.')[2]) == 2:
                newDate += ("20" + Dates[i].split('.')[2])
            else:
                newDate += (Dates[i].split('.')[2])
            newDates.append(newDate)
    print(newDates)

    Distances = dataset['Distance KM']
    DistancesMiles = dataset['Distance Miles']
    Durations = dataset['Duration']
    AvgPacesKM = dataset['Avg Pace KM']
    AvgPacesMiles = dataset['Avg Pace Miles']
    AvgSpeedsKMH = dataset['Avg Speed KMH']
    AvgSpeedsMPH = dataset['Avg Speed MPH']
    ShowGraph.run(newDates, Durations, Distances, AvgSpeedsKMH, AvgSpeedsMPH, AvgPacesKM, AvgPacesMiles)


def ConvertDates(data):
    newdata = []
    for entry in data:
        newdate = entry[0].replace("-",".")

        newdata.append([newdate, entry[1], entry[2]])
    return newdata


def ConvertKM(data):
    newdata = []
    for entry in data:
        if "miles" in entry[1]:
            distancemiles = int(entry[1].split('miles')[0])
            distancekm = distancemiles * 1.609344
        else:

            distancekm = float(entry[1].split('km')[0])
            distancemiles = distancekm / 1.609344

        newdata.append([entry[0], round(distancekm, 2), round(distancemiles,2), int(entry[2])])
    return newdata


def AvgPace(data):
    newdata = []
    print(data)
    for entry in data:
    # goes through each run
        pacekm = round((entry[3] / entry[1]), 2)
        pacemiles = round((entry[3] / entry[2]), 2)
        # to find out minutes per mile and minutes per km, divide duration by distance for each run

        newdata.append([entry[0], entry[1], entry[2], entry[3], str(pacekm), str(pacemiles)])
    return newdata


def AvgSpeed(data):
    newdata = []
    for entry in data:
        seconds = entry[3] * 60
        AvgSpeedKMH = (round(entry[1] / (seconds/3600), 2))
        AvgSpeedMPH = (round((entry[2] / (seconds/3600)), 2))
        newdata.append([entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], AvgSpeedKMH, AvgSpeedMPH])
    return newdata

