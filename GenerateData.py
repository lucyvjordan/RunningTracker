import os, sys, csv
import pandas as pd
import ShowGraph

def WriteData(data, method):
    data = ConvertKM(data)
    data = AvgPace(data)
    data = AvgSpeed(data)


    if method == "new":
        NewData(data)

    else:
        AppendData(data)


def NewData(data):
    with open(os.path.join(sys.path[0],"newdata.csv"), mode="w", newline='') as csvfile:
        fieldnames = ["Date", "Distance KM", "Distance Miles", "Duration", "Avg Pace KM", "Avg Pace Miles", "Avg Speed KMH", "Avg Speed MPH"]
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for row in data:
            writer.writerow(row)
    ReadData("newdata.csv")



def AppendData(data):
    with open(os.path.join(sys.path[0],"newdata.csv"), mode="a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)
    ReadData("newdata.csv")


def ReadData(filename):
    dataset = pd.read_csv(os.path.join(sys.path[0], filename), index_col=0)
    Dates = [str(_) for _ in dataset.index]
    
    newDates = []
    for i in range(len(Dates)):
        newDate = ""
        if len(Dates[i]) != 10:
            print("HI")
            if len(Dates[i].split('/')[0]) == 1:
                newDate += ("0" + Dates[i].split('/')[0] + "/")
            else:
                newDate += (Dates[i].split('/')[0] + "/")
            if len(Dates[i].split('/')[1]) == 1:
                newDate += ("0" + Dates[i].split('/')[1] + "/")
            else:
                newDate += (Dates[i].split('/')[1] + "/")
            if len(Dates[i].split('/')[2]) == 2:
                newDate += ("20" + Dates[i].split('/')[2])
            else:
                newDate += (Dates[i].split('/')[2])
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


def ConvertKM(data):
    newdata = []
    for entry in data:
        if "miles" in entry[1]:
            distancemiles = int(entry[1].split('miles')[0])
            distancekm = distancemiles * 1.609344
        else:
            distancekm = int(entry[1].split('km')[0])
            distancemiles = distancekm / 1.609344
        newdata.append([entry[0], round(distancekm, 2), round(distancemiles,2), int(entry[2])])
    return newdata


def AvgPace(data):
    newdata = []
    for entry in data:
    # goes through each run
        pacekm = str(entry[3] / entry[1])
        pacemiles = str(entry[3] / entry[2])
        if "." in pacekm:
        # min per km
            minutes = pacekm.split('.')[0]
            # numbers after decimal is how much of the minute has gone as a decimal, not in seconds
            seconds = int(pacekm.split('.')[1]) * 60
            # convert it to seconds by multipling the decimal points by 60
            pacekm = minutes + "." + str(seconds)[0:2]
        if "." in pacemiles:
        # min per mile
            minutes = pacemiles.split('.')[0]
            seconds = int(pacemiles.split('.')[1]) * 60
            pacemiles = minutes + "." + str(seconds)[0:2]
        newdata.append([entry[0], entry[1], entry[2], entry[3], pacekm, pacemiles])
    return newdata


def AvgSpeed(data):
    newdata = []
    for entry in data:
        seconds = entry[3] * 60
        AvgSpeedKMH = (round(entry[1] / (seconds/3600), 2))
        AvgSpeedMPH = (round((entry[2] / (seconds/3600))/ 1.609344, 2))
        newdata.append([entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], AvgSpeedKMH, AvgSpeedMPH])
    return newdata

