import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
from matplotlib.widgets import RadioButtons, Cursor


def run(Dates, Durations, DistancesKM, DistancesMiles, AvgSpeedsKMH, AvgSpeedsMPH, AvgPacesKM, AvgPacesMiles):

    Selections = [Durations, DistancesKM, DistancesMiles, AvgSpeedsKMH, AvgSpeedsMPH, AvgPacesKM, AvgPacesMiles]
    # so that the values plotted on the y-axis can be changed

    fig, ax = plt.subplots(figsize = (10,5), dpi = 100, num="Running Tracker")
    # defines the subplots, and the window size and title
    plt.subplots_adjust(left=0.4, right = 0.88)
    # puts empty space to the left of the plot so that the buttons can go there


    converted_dates = list(map(datetime.datetime.strptime, Dates, len(Dates)*['%d/%m/%Y']))
    # converts the date strings to date objects

    plot, = ax.plot(converted_dates, Selections[0], marker = 'o', mfc = 'w', linestyle = 'dashed')
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

    fig.set_facecolor("#ffffcc")
    # changes background colour of plot

    average = round(sum(plot.get_ydata())/len(plot.get_ydata()),2)
    fig.text(0.025,0.3,"The average duration is " + str(average) + " minutes.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
    # finds the average for the y-attribute chosen and displays it to screen


    databuttonsloc = plt.axes([0.05, 0.4, 0.25, 0.5], facecolor='White')
    databuttons = RadioButtons(databuttonsloc, ('Durations (minutes)', 'Distances (km)', 'Distances (miles)', 'Average Speeds (km/h)', 'Average Speeds (mph)', 'Average Paces (min/km)', 'Average Paces (min/mile)'), active = 0)
    # creates and shows buttons so the user can choose what y-attribute is shown


    for i in range(len(Dates)):
        annot = ax.annotate("", xy = (0,0), bbox = dict(boxstyle = 'round4',fc='linen',ec='k',lw=1))
        individualdate = (plot.get_xdata()[i])
        datexcoord = mpl.dates.date2num(individualdate)

        annot.xy = (datexcoord, Durations[i])

        text = "({:},{:}{:})".format(Dates[i], " ", Durations[i])

        annot.set_text(text)
        annot.set_visible(True) 

    def onclickpoint(event):
        x = event.xdata
        y = event.ydata

        for i in range(len(Dates)):
            individualdate = (plot.get_xdata()[i])
            datexcoord = mpl.dates.date2num(individualdate)
            annot = ax.annotate("({:},{:}{:})".format(Dates[i], " ", plot.get_ydata()[i]), xy = (datexcoord, plot.get_ydata()[i]), bbox = dict(boxstyle = 'square', fc='#ffffcc', ec='#0052cc', lw=1))

            try: 
                if x - 2 < datexcoord < x + 2:
                    if y - 0.5 < plot.get_ydata()[i] < y + 0.5:
                        annot.set_visible(True)   
                        break

                for child in ax.get_children():
                        if isinstance(child, mpl.text.Annotation):
                            child.remove()
            except:
                for child in ax.get_children():
                        if isinstance(child, mpl.text.Annotation):
                            child.remove()
                


        fig.canvas.draw()
        plt.show()

    fig.canvas.mpl_connect('motion_notify_event', onclickpoint)

    def drawGraph(label):

        labeldict = {'Durations (minutes)': Durations,
        'Distances (km)': DistancesKM,
        'Distances (miles)': DistancesMiles, 
        'Average Speeds (km/h)': AvgSpeedsKMH, 
        'Average Speeds (mph)': AvgSpeedsMPH, 
        'Average Paces (min/km)': AvgPacesKM, 
        'Average Paces (min/mile)': AvgPacesMiles}
        # dictionary to link the labels to the equivalent data


        ax.set_ylabel(label, fontsize = 14)
        plot.set_ydata(labeldict[label])
        # the y-label and data is changed to whichever button was pressed
        average = round(sum(plot.get_ydata())/len(plot.get_ydata()),2)    
        # the average for the y data is found

        if label == "Durations (minutes)":
            # each if statement changes the average displayed
            fig.text(0.025,0.2,"The average duration is " + str(average) + " minutes.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
        
        elif label == "Distances (km)":
            fig.text(0.025,0.2,"The average distance is " + str(average) + "km.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  

        elif label == "Distances (miles)":
            fig.text(0.025,0.2,"The average distance is " + str(average) + " miles.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
    
        elif label == "Average Speeds (km/h)":
            fig.text(0.025,0.2,"The average speed is " + str(average) + "km/h.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
            
        elif label == "Average Speeds (mph)":
            fig.text(0.025,0.2,"The average speed is " + str(average) + "mph.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
            
        elif label == "Average Paces (min/km)":
            fig.text(0.025,0.2,"The average pace is " + str(average) + "min/km.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
            
        elif label == "Average Paces (min/mile)":
            fig.text(0.025,0.2,"The average pace is " + str(average) + "min/mile.", fontsize=12, color = 'w', bbox={"facecolor":"b", "alpha":0.5})  
    
        minyvalue = float(min(plot.get_ydata())) * 0.9
        maxyvalue = float(max(plot.get_ydata())) * 1.1
        ax.set_ylim(minyvalue, maxyvalue)
        # this finds the limits for the y-axis, it will be limited to 10% either side of the data

        del fig.texts[0]  
        # the average text is deleted to they do not stack on top of each other

        plt.draw()
        # the graph is updated with the changes


    databuttons.on_clicked(drawGraph)
    # when a button is clicked, the drawGraph function is called

    plt.show()
    # this opens the window to show the graph


