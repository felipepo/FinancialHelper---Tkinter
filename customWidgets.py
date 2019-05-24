import tkinter as tk
import tkinter.ttk as ttk

'''
Classes related to customized widgets
    OptionsMenu
    ButtonIcon
    OptionsButton
'''

class ButtonIcon(tk.Frame):
    #Class to create a button with an icon
    def __init__(self, parent, imgFile):
        tk.Frame.__init__(self, parent)
        self.img = tk.PhotoImage(file = imgFile)
        self.buttonWithIcon = tk.Button(parent, bd=0, image = self.img)
       
        self.buttonWithIcon.image = self.img
        self.buttonWithIcon.pack(side="left", fill="y")

class OptionsMenu(tk.Frame):
    #Class to create the dropdown menu
    def __init__(self, parent, titleStr, choices):
        # Create a Tkinter variable
        titleStrvar = tk.StringVar()
        titleStrvar.set(titleStr)
        tk.Label(parent, textvariable=titleStrvar, bg = "white").grid(row = 0, column = 1, sticky="nsew")

        self.dropMenu = OptionsButton(parent, choices, 1, 1)         

class OptionsButton(tk.Frame):
    #Class to create the dropdown menu
    def __init__(self, parent, choices, nrow, ncol):
        if len(choices) == 0:
            choices.append("Sem Conta")
        # Create a Tkinter variable
        self.tkvar = tk.StringVar(parent)

        # Dictionary with options
        self.tkvar.set(choices[0]) # set the default option
    
        self.popupMenu = ttk.Combobox(parent, textvariable = self.tkvar, values = choices, state = 'readonly')
        #self.popupMenu.config(bd=0, bg="white")
        self.popupMenu.grid(row = nrow, column =ncol, sticky="nsew")
        
        # link function to change dropdown
        #self.tkvar.trace('w', self.change_dropdown)
    # on change dropdown value
    #def change_dropdown(self, *args):
    #    print( self.tkvar.get() )

class EntryWithText(ttk.Entry):
    def __init__(self, parent, defaultstr, checkFunction, styleName):
        ttk.Entry.__init__(self, parent)
        self.styleName = styleName + '.TEntry'
        self.defaultstr = defaultstr
        self.entry = ttk.Entry(parent, style = self.styleName)
        self.entry.insert(0, self.defaultstr)
        self.entry.bind('<FocusIn>', lambda event: self.on_entry_click(self))
        self.entry.bind('<FocusOut>', lambda event: self.on_focusout(self, checkFunction))
        
    def on_entry_click(event, self):
        """function that gets called whenever entry is clicked"""
        if self.entry.get() == self.defaultstr:
            self.entry.delete(0, "end") # delete all the text in the entry
            self.entry.insert(0, '') #Insert blank for user input
            currStyle = ttk.Style()
            currStyle.configure(self.styleName,foreground = 'black')
            #entry.config(fg = 'black')

    def on_focusout(event, self, checkFunction):
        if self.entry.get() == '':
            currStyle = ttk.Style()
            currStyle.configure(self.styleName,foreground = 'grey')
            self.entry.insert(0, self.defaultstr)
            #entry.config(fg = 'grey')
        else:
            checkFunction()
