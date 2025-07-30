"""
Fallback config.json generator for main.py.
"""

import json
import os
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

global themes
themes = {
    "themes": {
        "selected": "",
        "types": {
            "Light": {
                "background": "#ffffff",
                "text": "#000000",
                "save_buttons": "#d5ffa8",
                "other_buttons": "#ffc7a8"
            },
            "Dark": {
                "background": "#1c1c1c",
                "text": "#ffffff",
                "save_buttons": "#0e2905",
                "other_buttons": "#291a05"
            }   #A Human...
        }       #A Monster...
    }           #WHATSAPP
}               #GORDON FREEMAN

class Main:
    def __init__(self):
        self.root = Tk()     #Make root
        self.root.iconify()  #Minimize root, out of sight out of mind
        self.root.protocol("WM_DELETE_WINDOW", self.uwu)    #Pretty much disable closing windows.
        #Get current directory
        self.current_dir = os.getcwd
        #Ask if you want to config
        begincreation = messagebox.askyesno(title="Config Creator",
                            message="Config.json, an essential file for Text Edit, was not found. Do you wish to create it now?",
                            icon="question")

        if begincreation:
            self.ask_questions()
    
    def uwu(self):
        """
        bad class
        """
        pass #Literally just skips the function.

    def beginlineenter(self):
        """
        The window of all time
        """
        #Get screen info.
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)
        y = (screen_height / 2) - (100 / 2)
        self.EntryWindow = Toplevel()
        self.EntryWindow.geometry('%dx%d+%d+%d' % (300, 100, x, y))  #Thanks, coderslegacy!
        self.EntryWindow.overrideredirect(True) #Get rid of window decor. Nuclear option.
        #EntryWindow.protocol("WM_DELETE_WINDOW", self.uwu) #Too far, even for me. I couldn't bare not having Alt+F4!


        thelabel = Label(self.EntryWindow,
                         text="Enter into the below line to set your begin line.")
        beginlineentry = Entry(self.EntryWindow)
        enterlineentry = Button(self.EntryWindow,
                                text="Save text entered for the beginning line.",
                                command=lambda: self.ReturnLineEntry(beginlineentry.get()))
        thelabel.grid(column=0, row=0)
        beginlineentry.grid(column=0, row=1)
        enterlineentry.grid(column=0, row=2)
        self.EntryWindow.wait_window()

    def ReturnLineEntry(self, contents):
        self.EntryWindow.destroy()  #Kill it!
        global begin_line
        begin_line = contents

    def writeconfig(self):
        settings = {
            'themes': {
                'selected': theme,
                'types': themes['themes']['types']
            },
            'string': {
                'begin_line': begin_line
            },
            'boolean': {
                'fasttrack': yesno_fasttrack
            }
        }
        with open('config.json', 'w') as config:
            json.dump(settings, config, indent=4)
        messagebox.showinfo(title="Congratulations!",
                            message="Congratulations! You now have a working config.json and can now launch Text Edit.",
                            icon="info")
        exit("Config ready for next runthrough.")
    def ask_questions(self):
        """
        Ask the questions.
        """
        global yesno_fasttrack
        global theme
        yesno_fasttrack = messagebox.askyesno(title="Enable fasttrack?",
                                              message=("Do you wish to enable fasttrack? It disables dialogue for particually dangerous actions."
                                                       + "\nFor example, you can clear everything without a warning box.")
                                            )
        self.beginlineenter()   #Define begin_line
        theme_bool = messagebox.askyesno(title="What theme would you like?",
                               message=("Text Edit allows the usage of custom themes. For now, you have access to a light and dark theme." +
                                    "\nDo you wish to use the dark theme?")
                                )
        if theme_bool:
            theme = "Dark"
        else:
            theme = "Light"
        
        confirmation = messagebox.askyesno(title="All set!",
                                           message=("You have the following responses:\n" +
                                                    f"Fasttrack = {yesno_fasttrack}\n",
                                                    f"Beginning line = {begin_line}\n",
                                                    f"Theme chosen = {theme}\n" +
                                                    "Are you happy with these options?"))
        if confirmation:
            self.writeconfig()
        else:
            Main()
if __name__ == "__main__":
    try:
        with open("config.json", 'r') as config_check:
            print("config.json exists. If you need a new config, delete it first.")
        input("Press enter to exit.\n")
        exit("CONFIG.JSON exists")
    except FileNotFoundError:
        question = Main()