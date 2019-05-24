from tkinter import ttk

def setStyle(categoriesColor):
    #Set the program design
    currStyle = ttk.Style()
    newWindowBG = 'PaleTurquoise1'
    currStyle.theme_use('arc')
    
    #Main theme
    currStyle.configure('Main.TFrame', background = newWindowBG)
    currStyle.configure('Main.TLabelframe.LabelFrame', background = newWindowBG)
    currStyle.configure('Main.TLabelframe', background = newWindowBG)
    currStyle.configure('Main.TLabelframe.Label', background = newWindowBG, font = ('Arial',11))
    
    # Alert Style
    currStyle.configure('Alert.TLabel', foreground = 'red', background = newWindowBG)
    # New Window Style
    currStyle.configure('newWindow.TCombobox', background = newWindowBG)
    currStyle.configure('newWindow.TEntry', background = newWindowBG, foreground = 'black')
    currStyle.configure('newWindow.TLabel', background = newWindowBG, font = ('Arial',11), foreground = 'black')
    currStyle.configure('newWindow.TButton', background = newWindowBG)
    
    # Transaction box style
    for iCat in list(categoriesColor.keys()):
        categoryColor = categoriesColor[iCat]
        currStyle.configure(iCat + 'Box.TFrame', background = categoryColor)
        currStyle.configure(iCat + 'Box.TLabel', background = categoryColor, font = ('Arial',10), foreground = 'black')
        currStyle.configure(iCat + 'Date.TLabel', background = categoryColor, font = ('Arial',9, 'italic'), foreground = 'black')
        currStyle.configure(iCat + 'Acc.TLabel', background = categoryColor, font = ('Arial',10), foreground = 'black')
        currStyle.configure(iCat + 'NegVal.TLabel', background = categoryColor, font = ('Arial', 11, 'bold'), foreground = 'red')
        currStyle.configure(iCat + 'PosVal.TLabel', background = categoryColor, font = ('Arial', 11, 'bold'), foreground = 'green')
        currStyle.configure(iCat + 'Cat.TLabel', background = categoryColor, font = ('Helvetica',10), foreground = 'black')
        currStyle.configure(iCat + 'Comment.TLabel', background = categoryColor, font = ('Arial', 10, 'underline'), foreground = 'black')

def updateCategoryStyle(currCat, categoryColor):
    currStyle = ttk.Style()
    currStyle.configure(currCat + 'Box.TFrame', background = categoryColor)
    currStyle.configure(currCat + 'Box.TLabel', background = categoryColor, font = ('Arial',10), foreground = 'black')
    currStyle.configure(currCat + 'Date.TLabel', background = categoryColor, font = ('Arial',9, 'italic'), foreground = 'black')
    currStyle.configure(currCat + 'Acc.TLabel', background = categoryColor, font = ('Arial',10), foreground = 'black')
    currStyle.configure(currCat + 'NegVal.TLabel', background = categoryColor, font = ('Arial', 11, 'bold'), foreground = 'red')
    currStyle.configure(currCat + 'PosVal.TLabel', background = categoryColor, font = ('Arial', 11, 'bold'), foreground = 'green')
    currStyle.configure(currCat + 'Cat.TLabel', background = categoryColor, font = ('Helvetica',10), foreground = 'black')
    currStyle.configure(currCat + 'Comment.TLabel', background = categoryColor, font = ('Arial', 10, 'underline'), foreground = 'black')
