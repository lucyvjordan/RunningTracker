
import tkinter as tk
from tkinter import ttk, IntVar, filedialog
from tkcalendar import DateEntry
import GenerateData  
import sys

class Menu(tk.Tk):
    def __init__(self):

        super().__init__()

        self.runs = []
        # array will store all runs added        
        self.filename = ""

        self.frontColour = "#e6e6e6"
        self.backColour = "white"
        self.textColour = "black"
        # this is the initial colour scheme, can be changed by user

        self.geometry("450x500")
        self.title("Running Tracker Menu")

        self.configure(background=self.backColour)

        self.grid_rowconfigure((0,1,2), weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        # sets the columns and rows to expand if there is empty space


        self.radiostyle = ttk.Style()            
        self.radiostyle.configure('Radio.TRadiobutton', background=self.frontColour, foreground=self.textColour)
        # defines a style for the radio buttons

        self.labelstyle = ttk.Style()            
        self.labelstyle.configure('Label.TLabel', background=self.frontColour, foreground=self.textColour)  
        # defines a style for the labels

        self.title_label = ttk.Label(master=self, text="Running Tracker Main Menu", style= 'Label.TLabel', 
        font=("Georgia", 20, 'bold', 'underline'), borderwidth = 5, anchor="center")
        self.title_label.grid(row=0, column=0, padx=5, pady=5, columnspan = 2, sticky = "nsew") # sticky makes it expand to stick to the 4 cardinal directions
        # this label is the main title of the program, it is at the top of the screen

        self.side_frame = tk.Frame(master=self, background=self.frontColour)
        self.side_frame.grid(row=1, column=0, padx=5, pady=3, rowspan=2, sticky="nsew")
        # this frame will be used to contain the widgets in the left panel

        self.side_buttons = Buttons(master=self.side_frame, new = "New Graph", load="Load Graph", quit="Quit Tracker") # the class takes an undefined set of parameters, each of which details a button to be added
        self.side_buttons.pack(fill = "x", padx=5, pady=5)
        # these buttons in the left panel are made by creating an instance of the Button class, which creates a button frame.

        self.combobox = ttk.Combobox(master=self.side_frame, values=["Light", "Dark"])
        self.combobox.set("Light")
        self.combobox.pack(fill = "x", padx=5, pady=5)
        # this combobox allows the user to change between a light and dark colour setting, at default it is set to light
        self.combobox.bind('<<ComboboxSelected>>', self.changeColours)
        # when the value in the box is changed, a function is called which changes all the colours of the widgets

        self.appending = tk.Message(master=self.side_frame, text="", font = ("Georgia", 10), bg= "#e6e6e6", foreground=self.textColour, borderwidth=5, anchor="center")
        self.appending.pack(fill="x", padx=5, pady=5)

        self.error = tk.Message(master=self.side_frame, text="", font=("Georgia", 10), bg="#e6e6e6", foreground = "red", borderwidth=5, anchor = "center")
        self.error.pack(fill="x", padx=5, pady=5)

        self.main_frame = tk.Frame(master=self, background=self.frontColour)
        self.main_frame.grid(row=1, column=1, padx=5, pady=5, rowspan=3, sticky="nsew") # the rowspan is set to 3 so it fills up the whole of the screen vertically
        # this frame contains all of the main widgets where the data will be entered. 

        self.main_frame.grid_rowconfigure((0,1,2), weight=1)
        self.main_frame.grid_columnconfigure((0,1), weight=1)
        # sets the columns and rows to expand if there is empty space


        self.description = tk.Message(master=self.main_frame, text="Welcome to the Running Tracker!\nWhen you have finished entering your data, click 'Show Graph' to see your progress plotted against multiple statistics! Next time, simply press 'Load Graph' to continue tracking your runs.", font=("Georgia", 9), bg="#d1d1e0", foreground = self.textColour, 
        borderwidth = 5)
        self.description.grid(padx=5, pady=5, row=0, column=0, columnspan=2, sticky="ew")
        # this message outlines the functions of the program to the user

        self.bind("<Configure>", self.resize_messages)
        # when the size of the window is changed, the resize_description function is called to change the width of the text in the box

        self.run_label = ttk.Label(master=self.main_frame, text=("Data for Run %s:" %(str(len(self.runs) + 1))), font = ("Georgia", 12, 'underline'), style='Label.TLabel', borderwidth = 5, anchor="center")
        self.run_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        # this label uses the runs array to show which run the user is entering data for

        self.date_label = ttk.Label(master=self.main_frame, text="Date:", font=("Georgia", 10), style = 'Label.TLabel', borderwidth = 5)
        self.date_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")


        self.date = DateEntry(master=self.main_frame, background='#d1d1e0', foreground = "black", date_pattern = "dd-mm-yyyy") 
        # allows the user to enter the date of the run
        # i would like to change this so it is default to the current date
        self.date.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    

        self.distance_label = ttk.Label(master=self.main_frame, text="Distance:", font=("Georgia", 10), style='Label.TLabel', borderwidth = 5)
        self.distance_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        vcmd = (self.register(self.validate))        
        # creates a validate command, the validate function is run when this command is used
        self.distance = tk.Entry(master=self.main_frame, validate="key", validatecommand=(vcmd, "distance", '%P'))
        # the validate command is used when the user tries to enter text, the function makes sure only numbers are entered
        self.distance.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
    
        self.var = IntVar()
        self.km_button = ttk.Radiobutton(master=self.main_frame, text="KM", variable=self.var, value=1, style='Radio.TRadiobutton').grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.miles_button = ttk.Radiobutton(master=self.main_frame, text="Miles", variable=self.var, value=2, style='Radio.TRadiobutton').grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        # radio buttons to choose the units for the distance of the run, only one can be chosen at any time
        self.var.set(1)
        
        self.duration_label = ttk.Label(master=self.main_frame, text="Duration (minutes):", font=("Georgia", 10), style='Label.TLabel', borderwidth = 5)
        self.duration_label.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        self.duration = tk.Entry(master=self.main_frame, validate="key", validatecommand=(vcmd, "duration", '%P'))
        self.duration.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")
    
        self.bottom_buttons = Buttons(master=self.main_frame, add="Add Data Point", show="Show Graph")
        self.bottom_buttons.grid(row=6, column=0, padx=5, pady=5, columnspan=2, sticky="nsew")
        # more buttons, fills the frame horizontally
    

    def resize_messages(self, event):
        self.description.configure(width= (self.description.winfo_width() - 15))
        self.error.configure(width= (self.error.winfo_width() - 15))
        self.appending.configure(width= (self.error.winfo_width() - 15))
        # changes the width of the text in the description box dynamically depending on the size of the widget after resizing the window


    def changeColours(self, event):

        if self.combobox.get() == "Light":
            self.frontColour = "#e6e6e6"
            self.backColour = "white"
            self.textColour = "black"
            self.purpleBackground = "#d1d1e0"           
        else:
            self.frontColour = "#737373"
            self.backColour = "black"
            self.textColour = "white"
            self.purpleBackground = "purple"
        # sets colour variables depending on which setting chosen

        for section in self.winfo_children():
        # finds all the children of the main window (so the title, and both frames (side and main))
            try:
                section.configure(background=self.frontColour)
                section.configure(foreground=self.textColour)
            except:
            # not all the children will have a foreground setting as this is to do with text, so this prevents an error being raised
                pass

        self.configure(background=self.backColour)
        # changes the background colour of the window
        self.description.configure(background = self.purpleBackground, foreground = self.textColour)
        self.bottom_buttons.configure(background=self.purpleBackground)
        self.side_buttons.configure(background=self.purpleBackground)
        self.error.configure(background=self.frontColour)
        self.appending.configure(background=self.frontColour)
    
        self.labelstyle.configure('Label.TLabel', background=self.frontColour, foreground=self.textColour)
        self.radiostyle.configure('Radio.TRadiobutton', background=self.frontColour, foreground=self.textColour)
        # changes the colour schemes of the two styles defined for the labels and radio buttons

        for button in self.bottom_buttons.winfo_children():
            button.configure(background=self.backColour, foreground = self.textColour)
        for button in self.side_buttons.winfo_children():
            button.configure(background=self.backColour, foreground = self.textColour)
        # goes through each button in the both button frames, means that i dont need to know how many buttons are in each

    def validate(self, entry, text):
        if text == "":
            return True
            # checking whether it is "" allows users to backspace the first character
        
        if text[-1] == ".":
            # if they are trying to enter a decimal point
            if text.count(".") == 1 and text != "." and entry == "distance":
                # only allowed to enter if there is no decimal point yet, it is not the first character entered and it is in the distance field
                if len(text) < 5:
                    # ensures the decimal point isnt the final character
                    return True
        
        if text[-1].isnumeric():
            if len(text) < 6:
            # if the text attempting to be entered is an integer, and the text in the box is less than 6 characters long, then it is allowed to enter
                return True
        
        return False


class Buttons(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        # *args and **kwargs allows for undefined number of parameters to be passed, this means different button frames can have a different number of buttons
 
        super().__init__(master)
        # a frame is created within the master frame that has been passed as a parameter

        self.buttons = []
        # will keep track of all the buttons that needs to be added to the window
        self.configure(background="#d1d1e0")
        # changes the background of the buttons frame

        for key, value in kwargs.items():
            # the kwargs passed contain the details needed for the button; the key will be passed to the actions function and the value will be the text shown on the button
            self.buttons.append(tk.Button(master=self, command= lambda action=key: self.actions(action), 
            text=value, foreground = "black", background="white", font=("Georgia", 15), activebackground='#94d4be'))
            # active background changes the colour of the button when it is pressed
        
        for button in self.buttons:
            button.pack(fill = "x", padx=10, pady=10)
            # each button fills the frame horizontally


    def actions(self, action):
        # this function contains the processes that occur when a button is pressed
        if action == "new":
            menu.filename = ""
            menu.runs = []
            menu.run_label.configure(text=("Data for Run %s:" %(str(len(menu.runs) + 1))))
            menu.appending.configure(text="")  
            menu.error.configure(text="") 

        elif action == "load":
            menu.filename = filedialog.askopenfilename(initialdir=sys.path[0], title="Select A File", filetypes=(("csv files", "*.csv"),))
            menu.runs = []
            menu.run_label.configure(text=("Data for Run %s:" %(str(len(menu.runs) + 1))))
            menu.appending.configure(text="Appending to file: '%s'" % (menu.filename.split('/')[-1]))
            menu.error.configure(text="") 
        
        elif action == "quit":
            quit()

        elif action == "add":
            if menu.distance.get() == "" or menu.duration.get() == "" or menu.distance.get()[0] == "0" or menu.duration.get()[0] == "0" or menu.distance.get()[-1] == ".":
                # if either data entry is empty or starts with a 0 then the run is not added
                return
            if menu.var.get() == 1:
                # checks which radio button is selected so the unit can be appended with the distance
                menu.runs.append([menu.date.get(), menu.distance.get() + "km", menu.duration.get()])
            else:
                menu.runs.append([menu.date.get(), menu.distance.get() + "miles", menu.duration.get()])
            menu.run_label.configure(text=("Data for Run %s:" %(str(len(menu.runs) + 1))))
            # the text on screen which says which run is being entered for is updated
            menu.error.configure(text="") 
            menu.distance.delete(0, "end")
            menu.duration.delete(0, "end")
            # this clears the entry boxes

        elif action == "show":
            if len(menu.runs) < 2 and menu.filename == "": 
                menu.error.configure(text = "Please enter more runs before you generate your graph")
                return
            
            if menu.filename == "":
                menu.filename = filedialog.asksaveasfilename(initialdir=sys.path[0], defaultextension='.csv', filetypes = [("CSV File", ".csv")])
                GenerateData.WriteData(menu.filename, menu.runs, "new")
            
            GenerateData.WriteData(menu.filename, menu.runs, "append")
        


if __name__ == "__main__":
    # this is true when the program starts running
    menu = Menu()
    menu.mainloop()
    # keeps the menu running