"""
Text editor written in Python and utilizing the Tkinter framework.
Mostly pep-8 compliant.
By mostly, I mean excluding E124 and W503. I can't get those to work.
"""

# Cross-platform library used.
from tkinter import *
# Overwrites some Tk widgets with nicer looking ones.
from tkinter.ttk import *
# Messagebox: To ask stuff.
from tkinter.messagebox import *
# Filedialog: file explorer integration.
from tkinter.filedialog import *
# getcwd: Allows us to get the current working directory; path: get filenames.
from os import getcwd, path
# Used for the settings file.
import json

# Open up the config file (hopefully)
try:
    with open('config.json', 'r') as config:
        settings = json.load(config)    # Load all the variables.

except FileNotFoundError:
    configerror = ("Oh no! We couldn't find config.json."
                   " Do you want to set new settings?")
    yesno_config = askyesno(title="Config Error",
                            message=configerror,
                            icon='error')
    if yesno_config:
        # Gen_config helps generate a config if not there.
        import gen_config
        gen_config.Main()
    else:
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
            self.current_dir = getcwd()  # Our current working directory.
            self.filepath = "(Open a file first)"    # Placeholder Filepath.
            self.load_settings()    # Load settings

        # This used to be apart of the settings class, moved to actions.

        def load_settings(self):
            """
            ...Loads settings for Text Edit.
            """
            global fasttrack
            global begin_line
            global colours
            global themenames
            # Load fasttrack option
            fasttrack = (settings
                         ['boolean']
                         ['fasttrack']
                        )
            # "I wish there was a nice welcome message" The humble start line:
            begin_line = (settings
                          ['string']
                          ['begin_line']
                         )
            # Load theme names for the settings window
            themenames = list((settings
                               ['themes']
                               ['types']
                              ).keys()
                             )
            # What is our chosen theme?
            theme_chosen = (settings
                            ['themes']
                            ['selected']
                           )
            # Load chosen theme.
            colours = (settings
                       ['themes']
                       ['types']
                       [theme_chosen]
                      )

        def load_theme(self):
            """
            Loads the theme/colour config for Text Edit's widgets
            """
            # Wow, who thought that using ttk would be more complex than Tk?
            style = Style()
            # Set the window's background colour.
            root.configure(bg=colours
                           ['background']
                          )
            textbox.config(bg=colours
                           ['background'],
                           fg=colours
                           ['text']
                          )
            # Buttons affected here: save_as and justsave
            style.configure('savebutton.TButton',
                            background=colours
                            ['save_buttons']
                            )
            # Buttons affected here: clear_all, settingopen and openfile
            style.configure('otherbutton.TButton',
                            background=colours
                            ['other_buttons']
                           )

        def write_settings(self, category, name, value):
            """
            Writes settings to config.json
            """
            # For example, boolean's fasttrack equals True or False.
            settings[category][name] = value

            with open('config.json', 'w') as config:
                # A) Setting category to write to.
                # B) Where are we writing? C) Nice indent.
                json.dump(settings, config, indent=4)

        def onbuttonpress(self, type):
            """
            Button presses for the settings.
            """
            fasttracktitle = "WARNING: Really enable fasttrack?"
            fasttrackwarn = ("Fast-Track is an option which"
                             " skips confirmations for"
                             " potentially destructive actions."
                             " Enable anyways?")
            # What is the state of the fasttrack button?
            fasttrack_button_press = bool(self.fasttrackbutton_var.get())
            # If we want to change fasttrack and it's disabled,
            if fasttrack_button_press and type == 'fasttrack':
                # Prevent multiple messageboxes by disabling the button.
                self.fasttrackbutton.config(state=DISABLED)
                # Ask ARE YOU SURE THIS WILL BE VERY BAD AND OR TERRIBLE
                yesno_fasttrack = askyesno(title=fasttracktitle,
                                           message=fasttrackwarn,
                                           icon='warning')
                # Re-enable the button.
                self.fasttrackbutton.config(state=NORMAL)
                # If user wants to use FASTTRACK
                if yesno_fasttrack:
                    # Enable fasttrack
                    self.write_settings('boolean', 'fasttrack', True)

            # Oh wait, fasttrack is enabled and we want to disable it?
            elif not fasttrack_button_press and type == 'fasttrack':
                # Disable fasttrack.
                self.write_settings('boolean', 'fasttrack', False)

            # We want to set up the new begin line?
            elif type == "beginline":
                # Get the current begin line.
                linebegin = self.beginlineentry.get()
                # Write the new line
                self.write_settings('string', 'begin_line', linebegin)

            # We want to set up the new theme?
            elif type == "settheme":
                # Set the message for the infobox
                themeinfo = ("Theme will take effect"
                             " after program restart.")
                # Get the chosen theme.
                chosentheme = self.themeselect.get()
                # Write the settings.
                self.write_settings('themes', 'selected', chosentheme)
                # Show why the theme hasn't taken effect yet.
                showinfo(title='Information',
                         message=themeinfo,
                         icon='info')
            # Reload checkbox
            self.fasttrackbutton_var.set(int(settings
                                             ['boolean']
                                             ['fasttrack']
                                            ))
            # Reload settings
            self.load_settings()

        def settings_window(self):
            """
            Start a new window for Settings.
            Called exclusively by settingopen button.
            """
            settingopen.config(state=DISABLED)  # Disable the button
            # Setting up Settings window.
            # Create a new sub-window. Different to just Tk().
            self.setWin = Toplevel()
            # Geometry of sub-window.
            self.setWin.geometry("300x100")
            # As seen in root, I hate resizing windows.
            self.setWin.resizable(False, False)
            # Title of sub-window.
            self.setWin.title("Text Edit Settings")
            # "Hey, Window Manager, this is a child of root!"
            self.setWin.transient(root)
            # Grab the events only for this window.
            self.setWin.grab_set()
            # Puts subwindow into the spotlight. Above root.
            self.setWin.focus_set()

            # Setting up widgets
            # Subwindow's frame for widgets.
            self.settings_frame = Frame(self.setWin)
            # The below button's boolean value. Tick yes or no.
            self.fasttrackbutton_var = IntVar(value=int(settings
                                                        ['boolean']
                                                        ['fasttrack']
                                                        ))
            ftb_var = self.fasttrackbutton_var
            # Checkbox for FASTTRACK.
            self.fasttrackbutton = Checkbutton(self.settings_frame,
                                               text='Toggle \'Fasttrack\'',
                                               variable=ftb_var,
                                               command=lambda:
                                               self.onbuttonpress('fasttrack')
                                              )
            self.heresthelineentry = Label(self.settings_frame,
                                           text="Enter begining line below.")
            # Enter text here (One Line).
            self.beginlineentry = Entry(self.settings_frame)
            # Insert the one line that's the begin line.
            self.beginlineentry.insert(1, begin_line)
            self.button_ble = Button(self.settings_frame,
                                     text="Set new beginning line.",
                                     command=lambda:
                                     self.onbuttonpress('beginline')
                                    )
            self.themeselect = Combobox(self.settings_frame,
                                        values=themenames,
                                        )
            self.button_ts = Button(self.settings_frame,
                                    text="Set theme.",
                                    command=lambda:
                                    self.onbuttonpress('settheme')
                                   )
            # Put widgets into grid
            # Set up window frame.
            self.settings_frame.grid(column=0, row=0)
            # Insert fasttrack Checkbox.
            self.fasttrackbutton.grid(column=0, row=0, sticky='w')
            # Insert line entry Label.
            self.heresthelineentry.grid(column=0, row=1, sticky='w')
            # Insert line entry Entry.
            self.beginlineentry.grid(column=0, row=2, sticky='w')
            # Insert button entry Button.
            self.button_ble.grid(column=1, row=2, sticky='w')
            # Insert theme select Combobox.
            self.themeselect.grid(column=0, row=3, sticky='w')
            # Insert theme select Button.
            self.button_ts.grid(column=1, row=3, sticky='w')

            # Executing Settings window.
            # Unlike mainloop, this lets the next statement take effect.
            self.setWin.wait_window()
            # Re-enable the Settings button.
            settingopen.config(state=NORMAL)

        # Actual actions that can be taken.

        def open_file(self):
            """
            Opens an explorer instance to select a file.
            """
            if not fasttrack:  # If fasttrack is not active
                yesno_open_message = ("This action will get rid of"
                                      " everything in the textbox. Continue?")
                # Confirm overwrite.
                yesno_open = askyesno(title="Really open file?",
                                      message=yesno_open_message,
                                      icon='question')
            else:   # If fasttrack is active (True)
                yesno_open = True   # Skip dialogue.

            if yesno_open:
                global filepath
                # Asks the user to open a file.
                filepath = askopenfilename(initialdir=self.current_dir,
                                           title="Select file to save to",
                                           filetypes=(("Text Files", "*.txt"),
                                                      ("All files", "*.*"))
                                          )
                # If filepath is not nothin'
                if filepath != '':
                    # Open file
                    file = open(filepath, "r")
                    # Read the contents of file
                    contents = file.read()
                    # Close the file.
                    file.close()
                    # Clear everything to make space for contents of file
                    self.clear_textbox(True)
                    # Insert contents of file.
                    textbox.insert("1.0", contents)
                    # Update filepath in Titlebar and Save To button
                    self.update_filepath(filepath)

        def clear_textbox(self, skipquestion):
            """
            Command for clearing the textbox.
            Utilizes fasttrack, which is why it's a large function.
            """
            yesno_clearall_message = (
                "Clearing everything gets rid of everything in the Textbox!"
                " No information will be written!"
            )
            # If given the instruction to skip question
            if skipquestion or fasttrack:
                # Skip below message
                yesno_clearall = True

            else:   # If fasttrack isn't active or skipquestion is True:
                yesno_clearall = askyesno(title="Really clear all?",
                                          message=yesno_clearall_message,
                                          icon='question'
                                         )

            if yesno_clearall:  # If yesno is Yes
                textbox.delete("1.0", END)  # CLEARS ALL DATA!

        def savetofile(self, filepath, skipquestion):
            """
            Main file-saving logic. Suprisingly sorta logical.
            """
            # The line below is multi-line because it wasn't PEP-8.
            overwrite_warning = ("This action will overwrite the file."
                                 " Continue?")
            yesno_overwrite = True  # Sets the overwrite call to be true.
            # But if the function doesn't get the skip signal,
            if not skipquestion and not fasttrack:
                yesno_overwrite = askyesno(title="Really overwrite?",
                                           message=overwrite_warning,
                                           icon='question')

            if yesno_overwrite:
                # Open chosen file
                filetosaveto = open(filepath, "w")
                # Get the chosen text
                texttowrite = textbox.get("1.0", END)
                # Write text
                filetosaveto.write(texttowrite)
                # Close chosen file
                filetosaveto.close()
                # Update buttons and title.
                self.update_filepath(filepath)

        def savefileas(self):
            """
            Function that literally just adds a file explorer
            context window before saving the file.
            """
            filepath = asksaveasfilename(confirmoverwrite=True,
                                         title="Save file as...",
                                         filetypes=(("Text Files", "*.txt"),
                                                    ("All Files", "*.*"))
                                        )
            if filepath != '':
                self.savetofile(filepath, True)

        def confirm_close(self):
            """
            Window that pops up to confirm your closing of the program.
            (Thanks, Matt Gregory from
            https://stackoverflow.com/questions/111155/!)
            """
            close_warning = ("Closing the program won't save anything"
                             " written down. Continue?")
            if fasttrack:
                confirm = True
            elif not fasttrack:
                confirm = askyesno(title="Really close program?",
                                   message=close_warning,
                                   icon="warning")
            # If confirm is true:
            if confirm:
                root.destroy()

        def update_filepath(self, new_filepath):
            """
            Updates the filepath and justsave button.
            """
            # Makes filepath a global variable.
            global filepath
            # Makes filepath... filepath.
            filepath = new_filepath
            # Get filename from filepath.
            filename = path.basename(filepath)
            max_length = 15
            # If filename is more than [max_length]...
            if len(filename) > max_length:
                # Cuts it off after 12 characters.
                short_filename = filename[:12] + "..."
                justsave.config(state=NORMAL, text=f"Save To {short_filename}")
            else:
                justsave.config(state=NORMAL, text=f"Save To {filename}")

            root.title(f"Text Edit[ing]: {filename}")


global root
global window_frame
# Assign a variable to be the Main function caller.
act = Main.Actions()
# How do we window?
root = Tk()
# Text Edit's title.
root.title("Text Edit[or]")
# Geometery blocks yo window into 650x400, compact enough to fit everything.
root.geometry("650x400")
# Prevents resizing of all sorts.
root.resizable(False, False)
# New frame to put our widgets into
window_frame = Frame(root)
# Sets up the frame onto the root window
window_frame.grid(column=0, row=0)

# Evil button (Clear All)
clear_all = Button(window_frame,
                   text="Clear Everything",
                   command=lambda: act.clear_textbox(False),
                   style='otherbutton.TButton')
# Good button (Save as)
save_as = Button(window_frame,
                 text="Save File As",
                 command=act.savefileas,
                 style='savebutton.TButton')
# Another good button.   (Save to)
justsave = Button(window_frame,
                  text=f"Save to {act.filepath}",
                  command=lambda: act.savetofile(filepath, False),
                  state=DISABLED,
                  style='savebutton.TButton')   # Button disabled at start.

# Button you set with. (Open Settings)
settingopen = Button(window_frame,
                     text="Settings",
                     command=act.settings_window,
                     style='otherbutton.TButton')

# This button is for opening files, could you tell?
openfile = Button(window_frame,
                  text="Open File",
                  command=act.open_file,
                  style='otherbutton.TButton')


# Setting up the things that let you type text.
scroller = Scrollbar(window_frame)              # scroller.
textbox = Text(window_frame,                    # Parent window
               width=80, height=25,             # Dimensions
               wrap=WORD,
               yscrollcommand=scroller.set)     # How it wraps, how it scrolls
textbox.insert("1.0", begin_line)               # <- Adds text initially.
scroller.config(command=textbox.yview)

# Setting up the widgets in the window. (God bless Grid)
# Columnspan is used here so that the buttons are above it, not beside it.
textbox.grid(column=0, row=1, columnspan=5, sticky="nsew")
# Scroller's also here
scroller.grid(column=5, row=1, sticky="ns")
# Top row, far left
save_as.grid(column=0, row=0, sticky="nsew")
# Top row, far middle left
justsave.grid(column=1, row=0, sticky="nsew")
# Top row, far middle middle.
openfile.grid(column=2, row=0, sticky="nsew")
# Top row, far middle right
settingopen.grid(column=3, row=0, sticky="nsew")
# Top row, far right
clear_all.grid(column=4, row=0, sticky="nsew")
# Set up the colours
act.load_theme()

# Reconfigures the widgets to be expandable
for i in range(6):
    window_frame.grid_columnconfigure(i, weight=1)
# Allow frame to expand (useful for the textbox)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
# Allow textbox to grow and scrolling to work.
window_frame.grid_rowconfigure(1, weight=1)

if __name__ == "__main__":
    # Grab the exit button click, ask yes or no.
    root.wm_protocol("WM_DELETE_WINDOW", act.confirm_close)
    # Start the main loop of Tkinter.
    root.mainloop()
