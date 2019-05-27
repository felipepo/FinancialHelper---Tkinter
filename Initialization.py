import tkinter as tk
import tkinter.ttk as ttk
import MainWindowClasses
import HomePageClasses
import AccountPageClasses
import Classes
import Plots
import Funs
import StyleFormat

'''
Initialize the application and set windows:
    MainWindow
    HomePage
    AccountPage
    CreditCardPage
'''

class MainWindow(tk.Frame):
    #Class to create the Window Base
    def __init__(self, parent):
        #Create Frame
        tk.Frame.__init__(self, parent)

        #Create Object with all accounts
        try:
            loadedData = Funs.loadData() #Loads the data from file
            self.allAcc = loadedData #Creates object from loaded data
        except:
            self.allAcc = Classes.AllAccounts() #Creates object from scratch
            self.allAcc.AddAcc("Todas")
        
        StyleFormat.setStyle(self.allAcc.categoriesColor)
        self.sideMenu = MainWindowClasses.SideMenu(parent, self) #Create Side Menu Object        
        self.statusBar = MainWindowClasses.StatusBar(parent) #Create Status Bar Object        
        self.toolBar = MainWindowClasses.ToolBar(parent) #Create ToolBar Object
        self.toolBarIcons = MainWindowClasses.ToolBarIcons(parent, self) #Create ToolBar with icons Object

        #Create Home Page Frame
        self.home = tk.Frame(parent)
        Funs.SetGridWeight(2, 2, self.home, [0])#, [], [0])
        self.homePage = HomePage(self)

        #Create Account Page Frame
        self.accPageFrm = ttk.Frame(parent, style = 'Main.TFrame')
        Funs.SetGridWeight(2, 2, self.accPageFrm)
        self.accPage = AccountPage(self)
        
        #Create Credit Card Page Frame
        self.ccPageFrm = tk.Frame(parent)
        Funs.SetGridWeight(1, 2, self.ccPageFrm)
        ccPage = CreditCardPage(self.ccPageFrm)        
 
        self.home.tkraise()
        self.home.grid(row=1,column=2, sticky="nsew")     
        self.accPageFrm.grid(row=1,column=2, sticky="nsew")
        self.ccPageFrm.grid(row=1,column=2, sticky="nsew")

class HomePage(tk.Frame):
    #Class to create the homepage
    def __init__(self, mainWinObj):      
        
        self.accFrame = HomePageClasses.AccountFrame(mainWinObj) #Create Frame Object for the account 
        self.ccFrame = HomePageClasses.CreditCardFrame(mainWinObj.home) #Create Frame Object for the Credit Card 
        self.bills = HomePageClasses.Bills(mainWinObj.home) #Create Status Bar Object
        mainPlot = Plots.HomeWindowGraph(mainWinObj.home, mainWinObj) #Create Graph Object for the HomePage

        self.accFrame.UpdateLabel("Todas")

class AccountPage(tk.Frame):
    #Class to create the page with detailed account information
    def __init__(self, mainWinObj):
        
        self.transFrame = AccountPageClasses.TransactionFrame(mainWinObj) # Frame where transactions appear
        self.controlFrame = AccountPageClasses.ControlFrame(mainWinObj) # Frame with the control buttons
        #self.plotFrame = AccountPageClasses.PlotFrame(mainWinObj) # Frame for the plots
        mainPlot = Plots.HomeWindowGraph(mainWinObj.accPageFrm, mainWinObj) #Create Graph Object for the HomePage, (row = 0, column = 1)
        
        #accLabel = tk.Label(parent, text="Account Page Frame", bg = "white")
        #accLabel.pack()
    
class CreditCardPage(tk.Frame):
    #Class to create the page with detailed credit card information
    def __init__(self, parent):
        ccLabel = tk.Label(parent, text="Credit Card Page Frame", bg = "white")
        ccLabel.pack()
