import tkinter as tk
import tkinter.ttk as ttk
import pdb #Importing Debugger
import Classes
import Funs
import newWinds
import customWidgets

'''Classes related to MainWindow, which means, classes that are persistently
present in the window. In here, we have the following classes:
MainWindow:
    StatusBar
    SideMenu
    ToolBar
    ToolBarIcons    
'''
class StatusBar(tk.Frame):
    #Class to create the StatusBar
    def __init__(self,parent):
        self.labelString = tk.StringVar()
        self.labelString.set("Status Bar...")
        self.status = tk.Label(parent, textvariable=self.labelString, bd=1, relief="sunken", anchor="w")
        self.status.grid(row = 2, column = 0, columnspan = 3, sticky="nsew")
    def Update(self,strText):
    #Function to update the Status Bar String
        self.labelString.set(strText)

class SideMenu(tk.Frame):
    #Class to create the side menu bar
    def __init__(self,parent, container):#, frm1, frm2):
        #Create Frame
        self.sidebar = tk.Frame(parent,bg="gray", bd=1, relief="sunken")
        self.sidebar.grid(row = 1, column = 0, sticky="nsew")

        #Create Buttons for the SideBar Menu
        self.accountPage = tk.Button(self.sidebar, text="Contas")#,command=self.Addfun)
        self.accountPage.bind("<Button-1>",lambda event: Funs.ShowWindow(container.accPageFrm))
		
        self.creditCardPage = tk.Button(self.sidebar, text="Cartão de Crédito")#,command=self.Addfun)
        self.creditCardPage.bind("<Button-1>",lambda event: Funs.ShowWindow(container.ccPageFrm)) 

        #Create the Button to Hide/Show the SideBar Menu
        self.hidebutton = tk.Button(parent, text="<<", anchor="n", command=self.Hide)
        self.showbutton = tk.Button(parent, text=">>", anchor="n", command=self.Show)

        #Place the buttons        
        self.accountPage.pack(side="top",fill="x")
        self.creditCardPage.pack(side="top",fill="x")
        
        self.hidebutton.grid(row = 1, column = 1, sticky="nsew")
                
    def Hide(self):
    #Function to Hide side menu bar
        self.sidebar.grid_forget()
        self.showbutton.grid(row = 1, column = 1, sticky="nsew")
        self.hidebutton.grid_forget()
        
    def Show(self):
    #Function to Show side menu bar
        self.sidebar.grid(row = 1, column = 0, sticky="nsew")
        self.hidebutton.grid(row = 1, column = 1, sticky="nsew")
        self.showbutton.grid_forget()

class ToolBar(tk.Frame):
    #Class to create the homepage base
    def __init__(self,parent):
        #Create main Menu
        menu = tk.Menu(parent)
        parent.config(menu=menu)
        
        #Create File submenu
        fileMenu = tk.Menu(menu, tearoff=0)        
        menu.add_cascade(label="File",menu=fileMenu) #Create buttons in menu Bar        
        fileMenu.add_command(label="Export to Excel", command=self.Export) #Create buttons for submenu
        
        #Create Options submenu
        optionsMenu = tk.Menu(menu, tearoff=0)        
        menu.add_cascade(label="Opções",menu=optionsMenu) #Create buttons in menu Bar        
        optionsMenu.add_command(label="Preferências", command=self.Preferences) #Create buttons for submenu
        
    def Export(self):
    #Export data to excel
        print('ok')
    def Preferences(self):
    #Open the preferences window
        newWinds.PreferencesWindow()

class ToolBarIcons(tk.Frame):
    #Class to create the homepage base
    def __init__(self, parent, mainWinObj):
        tk.Frame.__init__(self, parent)
        #Create Frame
        self.toolbar = tk.Frame(parent, bg="light gray")
        self.toolbar.grid(row = 0, column = 0, columnspan = 3, sticky="nsew")

        #Create Buttons with icons
        homeButton = customWidgets.ButtonIcon(self.toolbar, r"Icons\homeButton.png")
        homeButton.buttonWithIcon.bind("<Button-1>",lambda event: Funs.ShowWindow(mainWinObj.home))
        
        addExpense = customWidgets.ButtonIcon(self.toolbar, r"Icons\AddExpenseBank.png")
        addExpense.buttonWithIcon.bind("<Button-1>",lambda event: self.newTransaction(mainWinObj, 'In', "bank"))
        
        addRevenue = customWidgets.ButtonIcon(self.toolbar, r"Icons\AddRevenueBank.png")
        addRevenue.buttonWithIcon.bind("<Button-1>",lambda event: self.newTransaction(mainWinObj, 'Out', "bank"))
        
        transfer = customWidgets.ButtonIcon(self.toolbar, r"Icons\Transfer.png")
        transfer.buttonWithIcon.config(command = self.newTransfer)
        
        AddAcc = customWidgets.ButtonIcon(self.toolbar, r"Icons\AddAccBank.png")
        AddAcc.buttonWithIcon.bind("<Button-1>",lambda event: self.DelOrAddAccount(mainWinObj, "Add", "bank"))

        RemoveAcc = customWidgets.ButtonIcon(self.toolbar, r"Icons\RemoveAccBank.png")
        RemoveAcc.buttonWithIcon.bind("<Button-1>",lambda event: self.DelOrAddAccount(mainWinObj, "Del", "bank"))

        addExpense = customWidgets.ButtonIcon(self.toolbar, r"Icons\AddExpenseCC.png")
        addExpense.buttonWithIcon.bind("<Button-1>",lambda event: self.newTransaction(mainWinObj, 'In', "creditCard"))
        
        addRevenue = customWidgets.ButtonIcon(self.toolbar, r"Icons\AddRevenueCC.png")
        addRevenue.buttonWithIcon.bind("<Button-1>",lambda event: self.newTransaction(mainWinObj, 'Out', "creditCard"))
        
        AddAcc = customWidgets.ButtonIcon(self.toolbar, r"Icons\AddAccCC.png")
        AddAcc.buttonWithIcon.bind("<Button-1>",lambda event: self.DelOrAddAccount(mainWinObj, "Add", "creditCard"))

        RemoveAcc = customWidgets.ButtonIcon(self.toolbar, r"Icons\RemoveAccCC.png")
        RemoveAcc.buttonWithIcon.bind("<Button-1>",lambda event: self.DelOrAddAccount(mainWinObj, "Del", "creditCard"))

        test = customWidgets.ButtonIcon(self.toolbar, r"Icons\Transfer.png")
        test.buttonWithIcon.bind("<Button-1>",lambda event: self.printAccountsData(mainWinObj))

        cat = customWidgets.ButtonIcon(self.toolbar, r"Icons\EditTransfer.png")
        cat.buttonWithIcon.bind("<Button-1>",lambda event: self.editCategories(mainWinObj))

    def editCategories(self, mainWinObj):
        newWinds.CategoryWindow(mainWinObj)
        
    def newTransaction(self, mainWinObj, inOrOut, bank_or_creditCard="bank"):
        newWinds.TransactionWindowSqr(mainWinObj, inOrOut, bank_or_creditCard=bank_or_creditCard)
        
    def newTransfer(self):
        newWinds.TransferWindow()
        
    def DelOrAddAccount(self, mainWinObj, deloradd, bank_or_creditCard="bank"):
        if deloradd == "Add":
            newWinds.NewAccountWindow(mainWinObj, bank_or_creditCard=bank_or_creditCard)
        else:
            newWinds.DelAccountWindow(mainWinObj, bank_or_creditCard=bank_or_creditCard)

    def printAccountsData(self, mainWinObj):
        for acc in list(mainWinObj.allAcc.accountsObjs.keys()):
            print(acc)
            Funs.showdic(mainWinObj.allAcc.accountsObjs[acc].transactions)
