import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
from matplotlib.widgets import RadioButtons, Cursor


def run(Dates, Durations, DistancesKM, DistancesMiles, AvgSpeedsKMH, AvgSpeedsMPH, AvgPacesKM, AvgPacesMiles):

    fig, ax = plt.subplots(figsize = (10,5), dpi = 100, num="Running Tracker")
    # defines the subplots, and the window size and title
    plt.subplots_adjust(left=0.4, right = 0.88)
    # puts empty space to the left of the plot so that the buttons can go there

    converted_dates = list(map(datetime.datetime.strptime, Dates, len(Dates)*['%d/%m/%Y']))
    # converts the date strings to date objects

    plot, = ax.plot(converted_dates, Durations, marker = 'o', mfc = 'w', linestyle = 'dashed')
    # plots the points

    fig.autofmt_xdate()
    # rotates dates so they display nicer

    plt.tick_params(axis='both', which = 'major', labelsize = 11)
    # sets attributes for axis numbers

    plt.ylabel("Durations", fontsize = 14)
    plt.xlabel("Dates", fontsize = 14)
    ax.set_title("Running Tracker", loc = "left", fontsize = 20, color = 'blue')
    fig.text(0.65, 0.9, "Hover over a point to see exact details!", fontsize = 8, color="black")
    # sets titles for axis and plot

    minyvalue = float(min(plot.get_ydata())) * 0.9
    maxyvalue = float(max(plot.get_ydata())) * 1.1
    ax.set_ylim(minyvalue, maxyvalue)
    # this finds the limits for the y-axis, it will be limited to 10% either side of the data

    fig.set_facecolor("#ffffcc")
    # changes background colour of plot

    average = round(sum(plot.get_ydata())/len(plot.get_ydata()),2)
    fig.text(0.025, 0.2,"The average duration is " + str(average) + " minutes.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
    # finds the average for the y-attribute chosen and displays it to screen
    fig.text(0.025,0.1,"Your best duration is " + str(round(max(plot.get_ydata()), 2)) + "minutes.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
    


    databuttonsloc = plt.axes([0.05, 0.4, 0.25, 0.5], facecolor='White')
    databuttons = RadioButtons(databuttonsloc, ('Durations (minutes)', 'Distances (km)', 'Distances (miles)', 'Average Speeds (km/h)', 'Average Speeds (mph)', 'Average Paces (min/km)', 'Average Paces (min/mile)'), active = 0)
    # creates and shows buttons so the user can choose what y-attribute is shown


    def onclickpoint(event):
        x = event.xdata
        y = event.ydata

        for i in range(len(Dates)):
            individualdate = (plot.get_xdata()[i])
            datexcoord = mpl.dates.date2num(individualdate)
            annot = ax.annotate("({:},{:}{:})".format(Dates[i], " ", plot.get_ydata()[i]), xy = (datexcoord, plot.get_ydata()[i]), bbox = dict(boxstyle = 'square', fc='#ffffcc', ec='#0052cc', lw=1))
            annot.set_visible(False)
            # turning them all to invisible first, then making the one (if any) being hovered over visible
            try: 
                if x - 2 < datexcoord < x + 2:
                    if y - 0.5 < plot.get_ydata()[i] < y + 0.5:
                        annot.set_visible(True)   
                        break

                for child in ax.get_children():
                    if isinstance(child, mpl.text.Annotation):
                        child.remove()
                        # removes any annotations from screen that have previously been hovered over, but are no longer
            except:
                pass
                
        fig.canvas.draw()
        plt.show()

    fig.canvas.mpl_connect('motion_notify_event', onclickpoint)

    def drawGraph(label):
        # the button that is clicked is passed in as the label parameter

        labeldict = {'Durations (minutes)': Durations,
        'Distances (km)': DistancesKM,
        'Distances (miles)': DistancesMiles, 
        'Average Speeds (km/h)': AvgSpeedsKMH, 
        'Average Speeds (mph)': AvgSpeedsMPH, 
        'Average Paces (min/km)': AvgPacesKM, 
        'Average Paces (min/mile)': AvgPacesMiles}
        # dictionary to link the labels to the equivalent data

        unitsdict = {'Durations (minutes)': "duration minutes",
        'Distances (km)': "distance km",
        'Distances (miles)': "distance miles", 
        'Average Speeds (km/h)': "speed km/h", 
        'Average Speeds (mph)': "speed mph", 
        'Average Paces (min/km)': "pace min/km", 
        'Average Paces (min/mile)': "pace min/mile"}
        # so that displaying average and best stats can be done efficienctly with no repitition of code

        ax.set_ylabel(label, fontsize = 14)
        plot.set_ydata(labeldict[label])
        # the y-label and data is changed to whichever button was pressed

        average = round(sum(plot.get_ydata())/len(plot.get_ydata()),2)    
        # the average for the y data is found

        minyvalue = float(min(plot.get_ydata())) * 0.9
        maxyvalue = float(max(plot.get_ydata())) * 1.1
        ax.set_ylim(minyvalue, maxyvalue)
        # this finds the limits for the y-axis, it will be limited to 10% either side of the data

        fig.text(0.025,0.2,"Your average " + unitsdict[label].split()[0] + " is " + str(average) + unitsdict[label].split()[1] + ".", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
        if label== "Average Paces (min/km)" or label == "Average Paces (min/mile)":
            fig.text(0.025,0.1,"Your best " + unitsdict[label].split()[0] + " is " + str(round(min(plot.get_ydata()), 2)) + unitsdict[label].split()[1] + ".", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
        else:
            fig.text(0.025,0.1,"Your best " + unitsdict[label].split()[0] + " is " + str(round(max(plot.get_ydata()), 2)) + unitsdict[label].split()[1] + ".", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
        # displays average and best for stat chosen

        del fig.texts[1]
        del fig.texts[1]  
        # the previous average and best texts are deleted to they do not stack on top of each other
        # the second text is deleted (index 1) twice because index 0 refers to the text saying "hover over a point..."
        plt.draw()
        # the graph is updated with the changes


    databuttons.on_clicked(drawGraph)
    # when a button is clicked, the drawGraph function is called

    plt.show()
    # this opens the window to show the graph


