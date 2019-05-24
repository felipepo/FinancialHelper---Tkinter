import tkinter as tk
from tkinter import ttk
import customWidgets
import Funs

'''
Classes related to the Account Page
AccountPage Classes:
    TransactionFrame
    PlotFrame
    ControlFrame
'''

class TransactionFrame(tk.Frame):
    # Class to create the frame where the transactions will appear
    def __init__(self, mainWinObj):
        tk.Frame.__init__(self)
        self.mainWinObj = mainWinObj
        # Create Left Half Frame, where the filter and the transactions are placed
        leftFrame = ttk.Frame(mainWinObj.accPageFrm, style = 'Main.TFrame')
        Funs.SetGridWeight(1, 2, leftFrame, [], [0])

        # Create Frame for the transactions
        transFrame = tk.LabelFrame(leftFrame, text = "Transações",bg = 'PaleTurquoise1', labelanchor = 'n', borderwidth = 4)#, style = 'Main.TLabelframe')
        Funs.SetGridWeight(5, 0, transFrame, [], [0])
        self.transContainer = ContainerTransactions(transFrame)
        self.transContainer.setOfTransactions(mainWinObj)

        # Create Frame for the filters and butons
        filterFrame = tk.Frame(leftFrame)
        b = tk.Label(filterFrame, text = "Filter").pack()
        
        filterFrame.grid(row = 0, column = 0, sticky = 'nswe')
        transFrame.grid(row = 1, column = 0, sticky="nsew")
        leftFrame.grid(row = 0, column = 0, rowspan = 2, sticky="nsew", padx = 5)

class ContainerTransactions(tk.Frame):
    # Class reponsible for organizing and displaying the transactions
    def __init__(self, parent):
        tk.Frame.__init__(self)
        self.parent = parent
        self.currRow = 0
        self.currCol = 0
        self.transactions = {}
    def addTransaction(self, transObj):
        # Function to create a transaction object
        #downArr = tk.PhotoImage(file = 'Icons\\redArr.png')
        #upArr = tk.PhotoImage(file = 'Icons\\greenArr.png')
        valueStr = "R$ " + transObj.value
        valType = 'NegVal'
        if '.' not in valueStr:
            valueStr = valueStr + '.00'
        currCat = transObj.category
        currTrans = "trans" + str(len(self.transactions))
        # Create a frame for the transaction box
        self.transactions[currTrans] = ttk.Frame(self.parent, style = currCat + 'Box.TFrame', relief="sunken")
        Funs.SetGridWeight(1, 3, self.transactions[currTrans])
        
        fstRowFrame = ttk.Frame(self.transactions[currTrans], style = currCat + 'Box.TFrame')
        Funs.SetGridWeight(2, 1, fstRowFrame)
        lblDate = ttk.Label(fstRowFrame, anchor = 'e', text = transObj.date, style = currCat + 'Date.TLabel')
        lblCat = ttk.Label(fstRowFrame, anchor = 'w', text = transObj.category, style = currCat + 'Cat.TLabel')
        lblCat.grid(row = 0, column = 0, sticky="nswe", padx = 2, pady = 2)
        lblDate.grid(row = 0, column = 1, sticky="nswe", padx = 2, pady = 2)
        fstRowFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 2, pady = 2)
        
        scndRowFrame = ttk.Frame(self.transactions[currTrans], style = currCat + 'Box.TFrame')
        Funs.SetGridWeight(2, 1, scndRowFrame)
        lblAcc = ttk.Label(scndRowFrame, anchor = 'w', text = transObj.bankAccount, style = currCat + 'Acc.TLabel')
        if '-' not in valueStr:
            valType = 'PosVal'
        lblVal = ttk.Label(scndRowFrame, anchor = 'w', text = valueStr, style = currCat + valType + '.TLabel')
        #lblArrow = tk.Label(scndRowFrame, anchor = 'e', image = downArr)
        #lblArrow.image = downArr
        lblAcc.grid(row = 0, column = 0, sticky="nswe", padx = 2, pady = 2)
        lblVal.grid(row = 0, column = 1, sticky = 'nswe', padx = 2, pady = 2)
        #lblArrow.grid(row = 0, column = 2, sticky = 'nswe', padx = 2, pady = 2)
        scndRowFrame.grid(row = 1, column = 0, sticky = 'nswe', padx = 2, pady = 2)
        
        trdRowFrame = ttk.Frame(self.transactions[currTrans], style = currCat + 'Box.TFrame')
        Funs.SetGridWeight(1, 1, trdRowFrame)
        lblCom = ttk.Label(trdRowFrame, text = transObj.comment, style = currCat + 'Box.TLabel')
        lblCom.grid(row = 0, column = 0, sticky="nswe", padx = 2, pady = 2)  
        trdRowFrame.grid(row = 2, column = 0, sticky = 'nswe', padx = 2, pady = 2)      
        
        self.transactions[currTrans].grid(row = self.currRow, column = self.currCol, padx = 2, pady = 2, sticky = 'nswe')
        self.currCol += 1
        if self.currCol == 5:
            self.currCol = 0
            self.currRow += 1
    def setOfTransactions(self, mainWinObj):
        # Set all of the transactions at once
        allAccounts = list(mainWinObj.allAcc.accountsObjs.keys())
        for iAcc in allAccounts:
            allTransactions = list(mainWinObj.allAcc.accountsObjs[iAcc].transactions.keys())
            for iTrans in allTransactions:
                self.addTransaction(mainWinObj.allAcc.accountsObjs[iAcc].transactions[iTrans])

    def clearContainer(self):
        self.currRow = 0
        self.currCol = 0
        for iBox in list(self.transactions.keys()):
            self.transactions[iBox].grid_forget()

class ControlFrame(tk.Frame):
    def __init__(self, mainWinObj):
        tk.Frame.__init__(self)
        tempFrame = tk.Frame(mainWinObj.accPageFrm)
        tempFrame.grid(row = 1, column = 1, sticky = 'nswe')

        tempLabel = tk.Label(tempFrame, text = "BUTOES")
        tempLabel.grid(row = 0, column = 0, sticky = 'nswe')
