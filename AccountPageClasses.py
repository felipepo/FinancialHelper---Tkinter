import tkinter as tk
from tkinter import ttk
import customWidgets
import Funs
import newWinds
import Main
from PIL import Image, ImageTk

'''
Classes related to the Account Page
AccountPage Classes:
    TransactionFrame
    PlotFrame
    ControlFrame
    TransactionClass
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
        self.alltransFrame = tk.LabelFrame(leftFrame, text = "Transações",bg = 'PaleTurquoise1', labelanchor = 'n', borderwidth = 4)#, style = 'Main.TLabelframe')
        Funs.SetGridWeight(5, 0, self.alltransFrame, [], [0])
        self.transContainer = ContainerTransactions(self)
        self.transContainer.setOfTransactions()

        # Create Frame for the filters and butons
        filterFrame = tk.Frame(leftFrame)
        tk.Label(filterFrame, text = "Filter").pack()
        
        filterFrame.grid(row = 0, column = 0, sticky = 'nswe')
        self.alltransFrame.grid(row = 1, column = 0, sticky="nsew")
        leftFrame.grid(row = 0, column = 0, rowspan = 2, sticky="nsew", padx = 5)

class ContainerTransactions(tk.Frame):
    # Class reponsible for organizing and displaying the transactions
    def __init__(self, transWindow):
        tk.Frame.__init__(self)
        self.mainWinObj = transWindow.mainWinObj
        self.parent = transWindow.alltransFrame
        self.currRow = 0
        self.currCol = 0
        self.transactions = {}
        self.transaciontBoards = {}

    def addTransaction(self, transObj):
        # Function to create a transaction object
        currTrans = transObj.transID
        self.transactions[currTrans] = TransactionClass(transObj, self.parent, self.mainWinObj)
        self.transactions[currTrans].transFrame.grid(row = self.currRow, column = self.currCol, padx = 2, pady = 2, sticky = 'nswe')
        self.transactions[currTrans].transFrame.grid_propagate(False)
        self.currCol += 1
        if self.currCol == 5:
            self.currCol = 0
            self.currRow += 1

    def setOfTransactions(self):
        # Set all of the transactions at once
        allAccounts = list(self.mainWinObj.allAcc.accountsObjs.keys())
        for iAcc in allAccounts:
            allTransactions = list(self.mainWinObj.allAcc.accountsObjs[iAcc].transactions.keys())
            for iTrans in allTransactions:
                self.addTransaction(self.mainWinObj.allAcc.accountsObjs[iAcc].transactions[iTrans])

    def clearContainer(self):
        self.currRow = 0
        self.currCol = 0
        for iBox in list(self.transactions.keys()):
            self.transactions[iBox].grid_forget()

    def updateAllBoards(self):
        alltrans = list(self.transactions.keys())
        for iTransactionBoard in alltrans:
            updateFlag = self.transactions[iTransactionBoard].UpdateBoard()
            if not updateFlag:
                #self.transactions[iTransactionBoard].transFrame.grid_forget()
                self.transactions[iTransactionBoard].transFrame.destroy()
                del self.transactions[iTransactionBoard]

class TransactionClass(tk.Frame):
    def __init__(self, transObj, parent, mainWinObj):
        tk.Frame.__init__(self)
        self.mainWinObj = mainWinObj
        self.transID = transObj.transID
        valueStr = "R$ " + transObj.value
        self.valType = 'NegVal'
        if '.' not in valueStr:
            valueStr = valueStr + '.00'
        currCat = transObj.category
        self.transCat = tk.StringVar()
        self.transDate = tk.StringVar()
        self.transVal = tk.StringVar()
        self.transAcc = tk.StringVar()
        self.transComm = tk.StringVar()
        self.transCat.set(transObj.category)
        self.transDate.set(transObj.date)
        self.transVal.set(valueStr)
        self.transAcc.set(transObj.bankAccount)
        self.transComm.set(transObj.comment)

        # Create a frame for the transaction box
        self.transFrame = ttk.Frame(parent, style = currCat + 'Box.TFrame', relief="sunken", height = 100, width = 120)
        Funs.SetGridWeight(1, 3, self.transFrame)
        
        self.fstRowFrame = ttk.Frame(self.transFrame, style = currCat + 'Box.TFrame')
        Funs.SetGridWeight(2, 1, self.fstRowFrame)
        self.lblDate = ttk.Label(self.fstRowFrame, anchor = 'e', textvariable =self.transDate, style = currCat + 'Date.TLabel')
        self.lblCat = ttk.Label(self.fstRowFrame, anchor = 'w', textvariable = self.transCat, style = currCat + 'Cat.TLabel')
        
        self.scndRowFrame = ttk.Frame(self.transFrame, style = currCat + 'Box.TFrame')
        Funs.SetGridWeight(2, 1, self.scndRowFrame)
        self.lblAcc = ttk.Label(self.scndRowFrame, anchor = 'w', textvariable = self.transAcc, style = currCat + 'Acc.TLabel')
        if '-' not in valueStr:
            self.valType = 'PosVal'
        self.lblVal = ttk.Label(self.scndRowFrame, anchor = 'w', textvariable = self.transVal, style = currCat + self.valType + '.TLabel')
        
        self.trdRowFrame = ttk.Frame(self.transFrame, style = currCat + 'Box.TFrame')
        Funs.SetGridWeight(2, 1, self.trdRowFrame, [1])
        self.lblCom = ttk.Label(self.trdRowFrame, textvariable = self.transComm, style = currCat + 'Box.TLabel')
        buttonImage = Image.open(r'Icons\EditTransfer.png')
        buttonPhoto = ImageTk.PhotoImage(buttonImage) 
        self.editBtn = ttk.Button(self.trdRowFrame, image=buttonPhoto, cursor = "hand2", style = currCat + 'Box.TLabel')
        self.editBtn.image = buttonPhoto
        self.editBtn.bind("<Button-1>", lambda event: self.editCurrentTransaction())
        
        # First Row Frame
        self.lblCat.grid(row = 0, column = 0, sticky="nswe", padx = 2, pady = 2)
        self.lblDate.grid(row = 0, column = 1, sticky="nswe", padx = 2, pady = 2)
        self.fstRowFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 2, pady = 2)  
        # Second Row Frame
        self.lblAcc.grid(row = 0, column = 0, sticky="nswe", padx = 2, pady = 2)
        self.lblVal.grid(row = 0, column = 1, sticky = 'nswe', padx = 2, pady = 2)
        self.scndRowFrame.grid(row = 1, column = 0, sticky = 'nswe', padx = 2, pady = 2) 
        # Third Row Frame
        self.lblCom.grid(row = 0, column = 0, sticky="nswe", padx = 2, pady = 2)  
        self.editBtn.grid(row = 0, column = 1, sticky="nswe") 
        self.trdRowFrame.grid(row = 2, column = 0, sticky = 'nswe', padx = 2, pady = 2)
        
    def editCurrentTransaction(self):
        newWinds.TransactionWindowSqr(self.mainWinObj, "update", self)

    def UpdateBoard(self, bankAcc = "default"):
        if bankAcc == "default":
            bankAccount = self.lblAcc["text"]
        else:
            bankAccount = bankAcc
        try:
            transactionData = self.mainWinObj.allAcc.accountsObjs[bankAccount].transactions[self.transID]
            category = transactionData.category
            self.transCat.set(transactionData.category)
            self.transDate.set(transactionData.date)
            self.transVal.set(transactionData.value)
            self.transAcc.set(transactionData.bankAccount)
            self.transComm.set(transactionData.comment)
            self.transFrame["style"] = category + 'Box.TFrame'
            self.fstRowFrame["style"] = category + 'Box.TFrame'
            self.scndRowFrame["style"] = category + 'Box.TFrame'
            self.trdRowFrame["style"] = category + 'Box.TFrame'
            self.lblCat["style"] = category + 'Cat.TLabel'
            self.lblDate["style"] = category + 'Date.TLabel'
            self.lblVal["style"] = category + self.valType + '.TLabel'
            self.lblAcc["style"] = category + 'Acc.TLabel'
            self.lblCom["style"] = category + 'Box.TLabel'
            self.editBtn["style"] = category + 'Box.TLabel'
            return True
        except:
            return False

class ControlFrame(tk.Frame):
    def __init__(self, mainWinObj):
        tk.Frame.__init__(self)
        tempFrame = tk.Frame(mainWinObj.accPageFrm)
        tempFrame.grid(row = 1, column = 1, sticky = 'nswe')

        tempLabel = tk.Label(tempFrame, text = "BUTOES")
        tempLabel.grid(row = 0, column = 0, sticky = 'nswe')
