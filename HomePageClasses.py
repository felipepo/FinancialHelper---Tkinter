import tkinter as tk
import customWidgets
import Funs

'''
Classes related to the HomePage
HomePage Classes:
    AccountFrame
    CreditCardFrame
    Bills
'''
        
class AccountFrame(tk.Frame):
    #Class to create the frame for the account
    def __init__(self, mainWinObj):
        self.mainWinObj = mainWinObj
        #Create Frame
        group = tk.LabelFrame(mainWinObj.home,text="Contas", bd=4, bg = "white")
        group.grid(row = 0, column = 0, sticky="nsew")

        #Create DropDown Menu Object
        titleStr = "Escolha conta"
        self.choices =  list(mainWinObj.allAcc.accountsObjs.keys())
        if not self.choices:
            self.choices.append("")
        self.options = customWidgets.OptionsMenu(group, titleStr, self.choices)
        self.options.dropMenu.tkvar.trace('w',self.change_dropdown)

        #Create Labels
        moneySign = tk.Label(group, text = "R$", bg = "white")
        
        totalStr = str(mainWinObj.allAcc.totalAmount)
        self.valueStr = tk.StringVar()
        self.valueStr.set(totalStr)
        self.value = tk.Label(group, textvariable = self.valueStr, bg = "white")
        if totalStr[0] == "-":
            self.value.config(fg = "red")
        else:
            self.value.config(fg = "limegreen")

        #Place Labels
        moneySign.grid(row=2,column=0)
        self.value.grid(row=2,column=1)
    def UpdateOptions(self):
        self.choices =  list(self.mainWinObj.allAcc.accountsObjs.keys())
        self.options.dropMenu.popupMenu.config(values = self.choices)
    def UpdateLabel(self, accName):
        totalStr = str(self.mainWinObj.allAcc.accountsObjs[accName].totalAmount)
        if accName == "Todas":
            totalStr = str(self.mainWinObj.allAcc.totalAmount)
        self.valueStr.set(totalStr)
        if totalStr[0] == "-":
            self.value.config(fg = "red")
        else:
            self.value.config(fg = "limegreen")
    def change_dropdown(self, *args):
        c = []
        for arg in args:
            c.append(arg)
        accName = self.options.dropMenu.tkvar.get()
        self.UpdateLabel(accName)
        
        
class CreditCardFrame(tk.Frame):
    #Class to create the frame for the credit card
    def __init__(self,parent):
        #Create Frame
        group = tk.LabelFrame(parent,text="Cartão de Crédito", bg = "white")
        group.grid(row = 1, column = 0, sticky="nsew")

        #Set weights for the grids
        Funs.SetGridWeight(2, 3, group, [],[0,1,2])

        #Create DropDown Menu Object
        titleStr = "Escolha conta"
        choices =  ["OI","KO","NJ"]
        options = customWidgets.OptionsMenu(group, titleStr, choices)

        #Create Labels
        moneySign = tk.Label(group, text = "R$", bg = "white")
        valueStr = "-99"
        value = tk.Label(group, text = "99,99", bg = "white")
        if valueStr[0] == "-":
            value.config(fg = "red")
        else:
            value.config(fg = "limegreen")

        #Place Labels
        moneySign.grid(row=2,column=0, sticky="nsew")
        value.grid(row=2,column=1, sticky="nsew")                 
    
class Bills(tk.Frame):
    #Class to create the frame for the credit card
    def __init__(self,parent):
        #Create Frame
        group = tk.LabelFrame(parent,text="Pagamentos Futuros", bg = "white")
        group.grid(row = 1, column = 1, sticky="nsew")

        #Create Labels
        moneySign = tk.Label(group, text = "R$", bg = "white")
        value = tk.Label(group, text = "99,99", bg = "white")

        #Place Labels
        moneySign.grid(row=0,column=0)
        value.grid(row=0,column=1)
