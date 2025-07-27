"""
Text editor written in Python and utilizing the Tkinter framework.                                                         
"""

#Variable definition.
from tkinter import *                           #Cross-platform graphical library used.
from tkinter.ttk import *                       #Overwrites some Tk widgets with nicer looking ones.
from tkinter import messagebox, filedialog      #Messagebox: summon cool error windows; Filedialog: file explorer integration
from os import getcwd, path                     #getcwd: Allows us to get the current working directory; path: get filenames.
import json                                     #Used for the settings file.


#Open up the config file (hopefully)
try:
    with open('config.json', 'r') as config:
        settings = json.load(config)    #Load all the variables.

#NOTE: MAJOR todo HERE!!! fuck the config.
except FileNotFoundError:
    messagebox.askyesno(title="Config Error",
                         message="Oh no! We couldn't find config.json. Do you want to set new settings?",
                         icon='error')
    messagebox.showinfo(title="Laziness", detail="Uh oh! The developer's lazy and the program will now close regardless of option choosen. :P")
    exit("config.json not found.")

class Main:
    """
    Main function of the program.
    """
    class Actions:
        """
        All of the actions that the program can take.
        Mainly saving, new windows and what-not.
        """
        def __init__(self):
            self.current_dir = getcwd()  #Our current working directory.
            self.filepath = "(Open a file first)"    #Placeholder Filepath.
            self.load_settings()    #Load settings

        #This used to be apart of the settings class, moved to actions.

        def load_settings(self):
            """
            ...Loads settings for Text Edit.
            """
            global fasttrack
            global begin_line
            global colours
            global themenames
            fasttrack = (settings['boolean']['fasttrack'])      #Load fasttrack option
            begin_line = (settings['string']['begin_line'])     #"I wish there was a nice welcome message" The humble start line:
            themenames = list((settings['themes']['types']).keys())
            theme_chosen = settings['themes']['selected']
            colours = settings['themes']['types'][theme_chosen]

        def load_theme(self):
            """
            Loads the theme/colour config for Text Edit's widgets
            """
            style = Style() #Wow, who thought that using ttk would be more complex than Tk?
            root.configure(bg=colours['background'])
            textbox.config(bg=colours['background'], fg=colours['text'])
            #Buttons affected here: save_as and justsave
            style.configure('savebutton.TButton',
                            background=colours['save_buttons']
                            )
            #Buttons affected here: clear_all, settingopen and openfile
            style.configure('otherbutton.TButton',
                            background=colours['other_buttons'])

        def write_settings(self, category, name, value):
            """
            Writes settings to config.json
            """
            #For example, boolean's fasttrack equals True or False.
            settings[f'{category}'][f'{name}'] = value

            with open('config.json', 'w') as config:
                json.dump(settings, config, indent=4)   #A) Setting category to write to. B) What is the Var? C) Cool indent.

        def onbuttonpress(self, type):
            """
            Button presses for the settings.
            """
            #What is the state of the fasttrack button?
            fasttrack_button_press = bool(self.fasttrackbutton_var.get())
            #If we want to change fasttrack and it's disabled,
            if fasttrack_button_press and type == 'fasttrack':
                #Prevent multiple messageboxes by disabling the button.
                self.fasttrackbutton.config(state=DISABLED)
                #Ask ARE YOU SURE THIS WILL BE VERY BAD AND OR TERRIBLE
                yesno_fasttrack = messagebox.askyesno(title="WARNING: Really activate Fast-Track?",
                                    message="Fast-Track is an option which skips confirmations for potentially destructive actions. Enable anyways?")
                #Re-enable the button.
                self.fasttrackbutton.config(state=NORMAL)
                #If user wants to use FASTTRACK
                if yesno_fasttrack:
                    self.write_settings('boolean', 'fasttrack', True)   #Enable (reluctantly)
            #Oh wait, fasttrack is enabled and we want to disable it?
            elif not fasttrack_button_press and type == 'fasttrack':
                self.write_settings('boolean', 'fasttrack', False)  #Disable.
            #We want to set up the new begin line?
            elif type == "beginline":
                linebegin = self.beginlineentry.get()                   #Get the current begin line.
                self.write_settings('string', 'begin_line', linebegin)  #Write the new line

            elif type == "settheme":
                chosentheme = self.themeselect.get()
                self.write_settings('themes', 'selected', chosentheme)
                messagebox.showinfo(title='Information',
                                    message='Theme will take effect after program restart.',
                                    icon='info')

            self.fasttrackbutton_var.set(int(settings['boolean']['fasttrack'])) #Reload checkbox
            self.load_settings() #Reload settings

        def settings_window(self):
            """
            Start a new window for Settings.
            Called exclusively by settingopen button.
            """
            settingopen.config(state=DISABLED)  #Disable the button

            #Setting up Settings window.
            self.setWin = Toplevel()                    #Create a new sub-window. Different to just Tk().
            self.setWin.geometry("300x100")             #Geometry of sub-window.
            self.setWin.title("Text Edit Settings")     #Title of sub-window.
            self.setWin.transient(root)                 #"Hey, Window Manager, this is a child of root!"
            self.setWin.grab_set()                      #Grab the events only for this window.
            self.setWin.focus_set()                     #Puts subwindow into the spotlight. Above root.
            self.setWin.resizable(False, False)         #As seen in root, I hate resizing windows.

            #Setting up widgets
            self.settings_frame = Frame(self.setWin)    #Subwindow's frame for widgets.
            self.fasttrackbutton_var = IntVar(value=int(settings['boolean']['fasttrack']))  #The below button's boolean value. Tick yes or no.
            self.fasttrackbutton = Checkbutton(self.settings_frame,
                                               text='Toggle \'Fasttrack\'',
                                               variable=self.fasttrackbutton_var,
                                               command=lambda: self.onbuttonpress('fasttrack'))
            self.heresthelineentry = Label(self.settings_frame,
                                           text="Enter begining line below.")
            self.beginlineentry = Entry(self.settings_frame)    #Enter text here (One Line).
            self.beginlineentry.insert(1, begin_line)           #Insert the one line that's the begin line.
            self.button_ble = Button(self.settings_frame,
                                     text="Set new beginning line.",
                                     command=lambda: self.onbuttonpress('beginline'))
            self.themeselect = Combobox(self.settings_frame,
                                        values=themenames,
                                        )
            self.button_ts = Button(self.settings_frame,
                                    text="Set theme.",
                                    command=lambda: self.onbuttonpress('settheme'))
            #Put widgets into grid
            self.settings_frame.grid(column=0, row=0)                   #Set up window frame.
            self.fasttrackbutton.grid(column=0, row=0, sticky='w')      #Insert checkbox.
            self.heresthelineentry.grid(column=0, row=1, sticky='w')    #Insert line entry Label.
            self.beginlineentry.grid(column=0, row=2, sticky='w')       #Insert line entry Entry.
            self.button_ble.grid(column=1, row=2, sticky='w')           #Insert button entry Button.
            self.themeselect.grid(column=0, row=3, sticky='w')
            self.button_ts.grid(column=1, row=3, sticky='w')

            #Executing Settings window.
            self.setWin.wait_window()           #Unlike mainloop, this lets the next statement take effect.
            settingopen.config(state=NORMAL)    #Re-enable the button.
        
        #Actual actions that can be taken.

        def open_file(self):
            """
            Opens an explorer instance to select a file.
            """
            if not fasttrack:  #If fasttrack is not active
                yesno_open = messagebox.askyesno(title="Really open file?",
                                    message="This action will get rid of everything in the textbox. Continue?",
                                    icon='question')    #Confirm overwrite.
            else:   #If fasttrack is active (True)
                yesno_open = True   #Skip dialogue.
            
            if yesno_open == True:
                global filepath
                filepath = filedialog.askopenfilename(initialdir=self.current_dir,
                                        title="Select file to save to",
                                        filetypes=(("Text Files", "*.txt"), ("All files", "*.*"))
                                        )   #Asks the user to open a file.
                #If filepath is not nothin'
                if filepath != '':
                    file = open(filepath, "r")      #Open file
                    contents = file.read()          #Read the contents of file
                    file.close()                    #Close the file.
                    self.clear_textbox(True)        #Clear everything to make space for contents of file
                    textbox.insert("1.0", contents) #Insert contents of file.
                    self.update_filepath(filepath)  #Update filepath in Titlebar and Save To button
                
        def clear_textbox(self, skipquestion):
            """
            Command for clearing the textbox. 
            Utilizes fasttrack, which is why it's a large function.
            """
            if skipquestion:
                yesno_clearall = True
            elif fasttrack:
                yesno_clearall = True
                
            else:   #If fasttrack isn't active or skipquestion is True:
                yesno_clearall = messagebox.askyesno(title="Really clear all?",
                                    message="Clearing everything gets rid of everything in the Textbox! No information will be written!",
                                    icon='question'
                                    )
            
            if yesno_clearall:  #If yesno is Yes
                textbox.delete("1.0", END)  #CLEARS ALL DATA!

        def savetofile(self, filepath, skipquestion):
            """
            Main file-saving logic. Suprisingly sorta logical.
            """
            yesno_overwrite = True  #Sets the overwrite call to be true.
            if not skipquestion and not fasttrack:    #But if the function doesn't get the skip signal (skipquestion)
                yesno_overwrite = messagebox.askyesno(title="Really overwrite?",
                                                    message="This action will overwrite the file. Continue?",
                                                    icon='question')
            
            if yesno_overwrite:
                filetosaveto = open(filepath, "w")      #Open chosen file
                texttowrite = textbox.get("1.0", END)   #Get the chosen text
                filetosaveto.write(texttowrite)         #Write text
                filetosaveto.close()                    #Close chosen file
                self.update_filepath(filepath)          #Update buttons and title.

        def savefileas(self):
            """
            Function that literally just adds a file explorer
            context window before saving the file.
            """
            filepath = filedialog.asksaveasfilename(confirmoverwrite=True,
                                                title="Save file as...",
                                                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
                                                )
            if filepath != '':
                self.savetofile(filepath, True)
        
        def confirm_close(self):
            """
            Window that pops up to confirm your closing of the program.
            (Thanks, Matt Gregory from https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter!)
            """
            if fasttrack:
                confirm = True
            elif not fasttrack:
                confirm = messagebox.askyesno(title="Really close program?",
                                              message="Closing the program won't save anything written down. Continue?",
                                              icon="warning")
            #If confirm is true:
            if confirm:
                root.destroy()

        def update_filepath(self, new_filepath):
            """
            Updates the filepath and justsave button.
            """
            global filepath
            filepath = new_filepath
            filename = path.basename(filepath)
            max_length = 15
            if len(filename) > max_length:
                short_filename = filename[:12] + "..."    #Cuts it off after 12 characters.
                justsave.config(state=NORMAL, text=f"Save To {short_filename}")
            else:
                justsave.config(state=NORMAL, text=f"Save To {filename}")
            
            root.title(f"Text Edit[ing]: {filename}")


global root
global window_frame
act = Main.Actions()
root = Tk() #How do we window?
root.title("Text Edit[or]")
#Geometery blocks yo window into 650x400, compact enough to fit everything I want.
root.geometry("650x400")
root.resizable(False, False)        #Prevents resizing of all sorts.
window_frame = Frame(root)          #New frame to put our widgets into
window_frame.grid(column=0, row=0)  #Sets up the frame onto the root window

#Evil button (Clear All)
clear_all = Button(window_frame,
                   text="Clear Everything",
                   command=lambda: act.clear_textbox(False),
                   style='otherbutton.TButton')
#Good button (Save as)
save_as = Button(window_frame,
                 text="Save File As",
                 command=act.savefileas,
                 style='savebutton.TButton')
#Another good button.   (Save to)
justsave = Button(window_frame,
                  text=f"Save to {act.filepath}",
                  command=lambda: act.savetofile(filepath, False),
                  state=DISABLED,
                  style='savebutton.TButton')   #Button disabled at start.
                                        
#Button you set with. (Open Settings)
settingopen = Button(window_frame,
                  text="Settings",
                  command=act.settings_window,
                  style='otherbutton.TButton')

#This button is for opening files, could you tell?
openfile = Button(window_frame,
                  text="Open File",
                  command=act.open_file,
                  style='otherbutton.TButton')


#Setting up the things that let you type text.
scroller = Scrollbar(window_frame)         #scroller.
textbox = Text(window_frame,                                #Parent window
               width=80, height=25,                         #Dimensions
               wrap=WORD, yscrollcommand=scroller.set)      #How it wraps, how it scrolls
textbox.insert("1.0", begin_line)  #<- Adds text initially.
scroller.config(command=textbox.yview)

#Setting up the widgets in the window. (God bless Grid)
textbox.grid(column=0, row=1, columnspan=5, sticky="nsew")  #Columnspan is used here so that the buttons are above it, not beside it.
scroller.grid(column=5, row=1, sticky="ns")                 #Scroller's also here
save_as.grid(column=0, row=0, sticky="nsew")                #Top row, far left
justsave.grid(column=1, row=0, sticky="nsew")               #Top row, far middle left
openfile.grid(column=2, row=0, sticky="nsew")               #Top row, far middle middle.
settingopen.grid(column=3, row=0, sticky="nsew")            #Top row, far middle right
clear_all.grid(column=4, row=0, sticky="nsew")              #Top row, far right
act.load_theme()                                            #Set up the colours

#Reconfigures the widgets to be expandable
for i in range(6):
    window_frame.grid_columnconfigure(i, weight=1)  #fuck grid, actually
#Allow frame to expand.
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
window_frame.grid_rowconfigure(1, weight=1)         #Allow textbox to grow and scrolling to work.

if __name__ == "__main__":  
    root.wm_protocol("WM_DELETE_WINDOW", act.confirm_close) #Grab the exit button click, ask yes or no.
    root.mainloop()                                         #Start the main loop of Tkinter.