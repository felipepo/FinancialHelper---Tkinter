import tkinter as tk
import customWidgets
import Funs
import re
import tkinter.ttk as ttk
import tkinter.colorchooser as tkCol
import pdb #Importing Debugger
import StyleFormat
import time

'''
Classes related to new windows
    newWindow
    TransactionWindowSqr
    TransferWindow
    NewAccountWindow
'''
def getDate():
    clk = list(time.localtime())
    day = str(clk[2])
    month = str(clk[1])
    year = str(clk[0])
    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month
    dateVal = day + "/" + month + "/" +  year
    return dateVal


class newWindow(tk.Frame):
    #Class to create a new window
    def __init__(self):
        tk.Frame.__init__(self)
        self.newWindow = tk.Toplevel(self)
        self.newWindow.geometry("+800+300") #Set new Window Position
        self.newWindow.grab_set() #Set new window as modal
        self.newWindow.resizable(width = 'false', height = 'false')
        tk.Grid.rowconfigure(self.newWindow, 0, weight=1)
        tk.Grid.columnconfigure(self.newWindow, 0, weight=1)
        self.newWindowFrm = ttk.Frame(self.newWindow, style = 'Main.TFrame')
        self.newWindowFrm.grid(row = 0, column = 0, sticky = 'nswe')

#=========================================================================================
class TransactionWindowSqr(newWindow):
    #Class to create a window to add data for a transaction
    def __init__(self, mainWinObj, inOrout, currTransaction = ""):
        newWindow.__init__(self)
        self.inOrout = inOrout
        self.mainWinObj = mainWinObj
        self.newWindow.wm_title("Nova Transação")
        self.newWindow.geometry("400x200")
        Funs.SetGridWeight(3,6,self.newWindowFrm, [0, 1])
        if inOrout == "In" or inOrout == "Out":
            categoryVal = "default"
            dateVal = "default"
            totalVal = "default"
            accVal = "default"
            commVal = ""
        else:
            self.transObj = currTransaction
            categoryVal = currTransaction.lblCat["text"]
            dateVal = currTransaction.lblDate["text"]
            totalVal = currTransaction.lblVal["text"]
            accVal = currTransaction.lblAcc["text"]
            commVal = currTransaction.lblCom["text"]
            totalVal = totalVal.replace("R$ ", "")
            totalVal = totalVal.replace("-", "")
            totalVal = totalVal.replace(".00", "")
        
        #Category
        self.categoryLabel = ttk.Label(self.newWindowFrm, text = "Categoria",anchor = 'w', style = 'newWindow.TLabel')
        self.categoryLabel.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew', padx = 5, pady = 5)
        listOfCategories = list(self.mainWinObj.allAcc.categoriesColor.keys())
        if not listOfCategories:
            listOfCategories.append("")
        self.categoryDropMenu = customWidgets.OptionsButton(self.newWindowFrm, listOfCategories, 1, 0, categoryVal)
        self.categoryDropMenu.popupMenu.configure(style = 'newWindow.TCombobox')
        self.categoryDropMenu.popupMenu.grid(columnspan = 2, padx = 5)
        
        #Date - DD/MM/YYYY
        self.dateLabel = ttk.Label(self.newWindowFrm, text = "Data",anchor = 'w', style = 'newWindow.TLabel')
        self.dateLabel.grid(row = 0, column = 2, columnspan = 2, sticky = 'nsew', padx = 5, pady = 5)
        dateVal = getDate()
        self.dateEntry = customWidgets.EntryWithText(self.newWindowFrm, 'DD/MM/YYYY', self.checkDate, 'DateEntry', dateVal)
        self.dateEntry.entry.grid(row = 1, column = 2, columnspan = 2, padx = 5, ipady = 5, sticky = 'nsew')
        
        #Value - XX,XX
        self.valueLabel = ttk.Label(self.newWindowFrm, text = "Valor (R$)",anchor = 'w', style = 'newWindow.TLabel')
        self.valueLabel.grid(row = 3, column = 0, columnspan = 2, sticky = 'nsew', padx = 5, pady = (5,5))
        self.valueEntry = customWidgets.EntryWithText(self.newWindowFrm, '00.00', self.checkValue, 'ValueEntry', totalVal)
        self.valueEntry.entry.grid(row = 4, column = 0, columnspan = 2, padx = 5, ipady = 5, sticky = 'nsew')
        
        #Account
        self.accLabel = ttk.Label(self.newWindowFrm, text = "Conta",anchor = 'w', style = 'newWindow.TLabel')
        self.accLabel.grid(row = 3, column = 2, columnspan = 2, sticky = 'nsew', padx = 5, pady = (5,5))
        listOfAccounts = list(self.mainWinObj.allAcc.accountsObjs.keys())
        if not listOfAccounts:
            listOfAccounts.append("")
        else:
            del listOfAccounts[0]
        self.accDropMenu = customWidgets.OptionsButton(self.newWindowFrm, listOfAccounts, 4, 2, accVal)
        self.accDropMenu.popupMenu.configure(style = 'newWindow.TCombobox')
        self.accDropMenu.popupMenu.grid(columnspan = 2, padx = 5)
        
        #Comment
        self.commentLabel = ttk.Label(self.newWindowFrm, text = "Comentário",anchor = 'sw', style = 'newWindow.TLabel')
        self.commentLabel.grid(row = 5, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = (5,5))
        self.commentEntry = ttk.Entry(self.newWindowFrm, style = 'newWindow.TEntry')
        self.commentEntry.insert(0, commVal)
        self.commentEntry.grid(row = 6, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, ipady = 5, pady = (0,5))

        #Wrong date format label
        self.wrongDateLbl = ttk.Label(self.newWindowFrm, text = "Formato da data é DD/MM/YYYY", anchor = 'w', style = 'Alert.TLabel')
        
        self.getEntry = ttk.Button(self.newWindowFrm, text = "OK", style = 'newWindow.TButton')
        if inOrout == "update":
            self.getEntry.bind("<Button-1>", lambda event: self.updateTransaction())
        else:
            self.getEntry.bind("<Button-1>", lambda event: self.newTransaction())
        self.getEntry.grid(row = 5, column = 3, rowspan = 2,sticky = 'nswe', padx = 5, pady = (20,5))

    def newTransaction(self):
        category = self.categoryDropMenu.tkvar.get()
        value = self.valueEntry.entry.get()
        if self.inOrout == 'Out':
            value = '-' + value
        date = self.dateEntry.entry.get()
        bankAccount = self.accDropMenu.tkvar.get()
        comment = self.commentEntry.get()
        currTrans = self.mainWinObj.allAcc.AddTransaction(category, value, date, comment, bankAccount)
        if currTrans:
            currTransObj = self.mainWinObj.allAcc.accountsObjs[bankAccount].transactions[currTrans]
            self.mainWinObj.accPage.transFrame.transContainer.addTransaction(currTransObj)
            accName = self.mainWinObj.homePage.accFrame.options.dropMenu.tkvar.get()
            self.newWindow.destroy()
            self.mainWinObj.homePage.accFrame.UpdateLabel(accName)
        else:
            tk.messagebox.showinfo('Campo incorreto','Erro nos campos.')

    def updateTransaction(self):
        category = self.categoryDropMenu.tkvar.get()
        value = self.valueEntry.entry.get()
        if self.inOrout == 'Out':
            value = '-' + value
        date = self.dateEntry.entry.get()
        bankAccount = self.accDropMenu.tkvar.get()
        comment = self.commentEntry.get()
        updatedFlag = self.mainWinObj.allAcc.UpdateTransaction(self.transObj.transID, category, value, date, comment, bankAccount, self.transObj.lblAcc["text"])
        if updatedFlag:
            accName = self.mainWinObj.homePage.accFrame.options.dropMenu.tkvar.get()
            self.newWindow.destroy()
            self.mainWinObj.homePage.accFrame.UpdateLabel(accName)
        else:
            tk.messagebox.showinfo('Campo incorreto','Erro nos campos.')
        self.transObj.UpdateBoard(bankAccount)

    def checkDate(self):
        datePattern = re.compile(r'\d{2}/\d{2}/\d{4}\Z')
        matched = datePattern.match(self.dateEntry.entry.get())
        if not matched:
            self.wrongDateLbl.grid(row = 2, column = 2, columnspan = 2, sticky = 'nsew', padx = 5)
            #tk.messagebox.showinfo('Formato Data','A data foi escrita no formato errado.')
            return False
        else:
            self.wrongDateLbl.grid_forget()
            return True

    def checkValue(self):
        currValue = self.valueEntry.entry.get()
        try:
            float(currValue)
        except:
            msgStr = "Valor não é válido"
            print(msgStr)

#=========================================================================================
class TransferWindow(newWindow):
    #Class to create a window to add data for a transfer
    def __init__(self):
        newWindow.__init__(self)
        self.newWindow.wm_title("Dados da Transação")
        
        #Source Account
        self.accLabel = tk.Label(self.newWindow, text = "Origem")
        self.accLabel.grid(row = 0, column = 0)
        self.accDropMenu = customWidgets.OptionsButton(self.newWindow, ["ACC","nj","bh"], 1, 0)
        
        #Destination Account
        self.accLabel = tk.Label(self.newWindow, text = "Destino")
        self.accLabel.grid(row = 0, column = 1)
        self.accDropMenu = customWidgets.OptionsButton(self.newWindow, ["ACC","nj","bh"], 1, 1)
        
        #Value - XX,XX
        self.valueLabel = tk.Label(self.newWindow, text = "Valor (R$)")
        self.valueLabel.grid(row = 2, column = 0)
        self.valueEntry = tk.Entry(self.newWindow)
        self.valueEntry.grid(row = 3, column = 0)
        
        #Comment
        self.commentLabel = tk.Label(self.newWindow, text = "Comentário")
        self.commentLabel.grid(row = 4, column = 0, columnspan = 2)
        self.commentEntry = tk.Entry(self.newWindow)
        self.commentEntry.grid(row = 5, column = 0, columnspan = 2)
        
        getEntry = tk.Button(self.newWindow, text = "Ok")
        #getEntry.bind("<Button-1>", lambda event: CreateTransaction(caller)
        getEntry.grid(row = 5, column = 2)

#=========================================================================================
class AccountWindow(newWindow):
    #Class to create window for an account creation or removal
    def __init__(self, mainWinObj):
        newWindow.__init__(self)
        #Funs.SetGridWeight(1,1,self.newWindowFrm, [1])

        #Account Name
        self.valueLabel = ttk.Label(self.newWindowFrm, text = "Nome da conta", style = 'newWindow.TLabel')
        self.valueLabel.grid(row = 0, column = 0, sticky = 'nw', padx = 5, pady = 5)

        #Create OK Buttons
        self.okButton = ttk.Button(self.newWindowFrm, text = "Ok", width = 5, style = 'newWindow.TButton')
        self.okButton.grid(row = 1, column = 1, padx = 5, pady = 5)
    
#=========================================================================================
class NewAccountWindow(AccountWindow):
    #Class to create window where a new account is added
    def __init__(self, mainWinObj):
        AccountWindow.__init__(self, mainWinObj)
        self.newWindow.wm_title("Nova Conta")

        #Entry for account name
        self.valueEntry = ttk.Entry(self.newWindowFrm, style = 'newWindow.TEntry')
        self.valueEntry.focus()
        self.valueEntry.bind("<Return>", lambda event: self.newAccount(mainWinObj))
        self.valueEntry.grid(row = 1, column = 0, sticky = 'nsew', padx = 5, pady = 5)

        self.okButton.bind("<Button-1>", lambda event: self.newAccount(mainWinObj))

    def newAccount(self, mainWinObj):
        #Function to add a new account
        value = self.valueEntry.get()
        added = mainWinObj.allAcc.AddAcc(value)

        #Check if the account already exists
        if added:            
            mainWinObj.homePage.accFrame.UpdateOptions()
            self.destroy()
        else:
            tk.messagebox.showinfo('Conta Existente','A conta que você está tentando adicionar já existe.')
            #windObj.okButton.config(relief = "raised")

#=========================================================================================
class DelAccountWindow(AccountWindow):
    #Class to create window where a new account is added
    def __init__(self, mainWinObj):
        AccountWindow.__init__(self, mainWinObj)
        self.newWindow.wm_title("Remover Conta")

        listOfAccounts = list(mainWinObj.allAcc.accountsObjs.keys())
        if not listOfAccounts:
            listOfAccounts.append("")
        else:
            del listOfAccounts[0]

        self.accOptions = customWidgets.OptionsButton(self.newWindowFrm, listOfAccounts, 1, 0)
        self.accOptions.popupMenu.grid(padx = 5, pady = 5)

        self.okButton.bind("<Button-1>", lambda event: self.delAccount(mainWinObj))
    
    def delAccount(self, mainWinObj):
        #Function to add a new account
        value = self.accOptions.tkvar.get()
        added = mainWinObj.allAcc.DelAcc(value)

        #Check if the account already exists
        if added:            
            mainWinObj.homePage.accFrame.UpdateOptions()
            self.destroy()
        else:
            tk.messagebox.showinfo('Conta Existente','A conta que você está tentando adicionar já existe.')
            #self.okButton.config(relief = "raised")

#=========================================================================================
class PreferencesWindow(newWindow):
    #Class to create the preferences Window
    def __init__(self):
        newWindow.__init__(self)
        self.newWindow.wm_title("Preferências")
        self.lbl = tk.Label(self.newWindow, text = "Tela de preferências")
        self.lbl.pack()

#=========================================================================================
class CategoryWindow(newWindow):
    # Class to edit the categories
    def __init__(self, mainWinObj):
        newWindow.__init__(self)
        self.mainWinObj = mainWinObj
        self.newWindow.wm_title("Categorias")
        #self.newWindow.protocol("WM_DELETE_WINDOW", self.destroyFcn)
        Funs.SetGridWeight(1,2,self.newWindowFrm)
        listOfCategories = list(mainWinObj.allAcc.categoriesColor.keys())
        if not listOfCategories:
            listOfCategories.append("")
            firstColor = 'PaleTurquoise1'
        else:
            firstColor = mainWinObj.allAcc.categoriesColor[listOfCategories[0]]
            
        self.renameCat = tk.LabelFrame(self.newWindowFrm, background = 'PaleTurquoise1', text = "Renomear")
        Funs.SetGridWeight(3,1,self.renameCat)
        self.renameListMenu = customWidgets.OptionsButton(self.renameCat, listOfCategories, 0, 0)
        self.renameListMenu.popupMenu.configure(style = 'newWindow.TCombobox')
        self.newCatNameEntry = ttk.Entry(self.renameCat)
        self.renameCatButton = ttk.Button(self.renameCat, text = "Renomear", style = 'newWindow.TButton')
        self.renameCatButton.bind("<Button-1>", lambda event: self.renameCategory(mainWinObj))

        self.delCat = tk.LabelFrame(self.newWindowFrm, background = 'PaleTurquoise1', text = "Remover")
        Funs.SetGridWeight(3,1,self.delCat)
        
        self.delListMenu = customWidgets.OptionsButton(self.delCat, listOfCategories, 0, 0)
        self.delListMenu.popupMenu.configure(style = 'newWindow.TCombobox')

        self.removeCat = ttk.Button(self.delCat, text = "Del", style = 'newWindow.TButton')
        self.removeCat.bind("<Button-1>", lambda event: self.removeCategory(mainWinObj))
        
        self.addCat = tk.LabelFrame(self.newWindowFrm, background = 'PaleTurquoise1', text = "Adicionar")
        Funs.SetGridWeight(3,1,self.addCat)
        
        #self.newCatEntry = customWidgets.EntryWithText(self.addCat, 'Nova Categoria', self.emptyFcn, 'newWindow')
        self.newCatEntry = ttk.Entry(self.addCat)
        
        self.changeColor = tk.Label(self.addCat, text = '    ', bg = 'red')
        self.changeColor.bind("<Button-1>", lambda event: self.updateColorLabel(self.changeColor))
        
        self.createCat = ttk.Button(self.addCat, text = "Add", style = 'newWindow.TButton')
        self.createCat.bind("<Button-1>", lambda event: self.addCategory(mainWinObj))
        
        self.editCat = tk.LabelFrame(self.newWindowFrm, background = 'PaleTurquoise1', text = "Editar")
        Funs.SetGridWeight(2,1,self.editCat)
        self.currCatColor = tk.Label(self.editCat, text = '    ')
        self.currCatColor.bind("<Button-1>", lambda event: self.changeCatColor(mainWinObj))
        self.currCatColor.configure(bg = firstColor)
        
        self.catListMenu = OptionsButton(self.editCat, listOfCategories, 0, 0, mainWinObj, self.currCatColor)
        self.catListMenu.popupMenu.configure(style = 'newWindow.TCombobox')

        # Rename Category section
        self.renameCat.grid(row = 0, column = 0, sticky = 'nswe', padx = 5, pady = 5)
        self.renameListMenu.popupMenu.grid(columnspan = 1, padx = 5, pady = 5)
        self.newCatNameEntry.grid(row = 0, column = 2, sticky = 'nswe', padx = 5, pady = 5)
        self.renameCatButton.grid(row = 0, column = 3, sticky = 'nswe', padx = 5, pady = 5)

        # Remove Category section
        self.delCat.grid(row = 1, column = 0, sticky = 'nswe', padx = 5, pady = 5)
        self.delListMenu.popupMenu.grid(columnspan = 1, padx = 5, pady = 5)
        self.removeCat.grid(row = 0, column = 2, sticky = 'nswe', padx = 5, pady = 5)

        # Add category section
        self.addCat.grid(row = 2, column = 0, sticky = 'nswe', padx = 5, pady = 5)
        self.newCatEntry.grid(row = 0, column = 0, sticky = 'nswe', padx = 5, pady = 5)
        self.changeColor.grid(row = 0, column = 1, sticky = 'nswe', padx = 5, pady = 5)
        self.createCat.grid(row = 0, column = 2, sticky = 'nswe', padx = 5, pady = 5)

        # Edit Category section
        self.editCat.grid(row = 3, column = 0, sticky = 'nswe', padx = 5, pady = 5)
        self.catListMenu.popupMenu.grid(columnspan = 1, padx = 5, pady = 5)
        self.currCatColor.grid(row = 0, column = 1, sticky = 'nswe', padx = 5, pady = 5)

    def changeCatColor(self, mainWinObj):
        targetCategory = self.catListMenu.tkvar.get()
        color = tkCol.askcolor() 
        self.currCatColor.configure(bg = color[1])
        mainWinObj.allAcc.categoriesColor[targetCategory] = color[1]
        StyleFormat.updateCategoryStyle(targetCategory, color[1])
        
    def updateColorLabel(self, changeColor):
        color = tkCol.askcolor() 
        changeColor.configure(bg = color[1])
        
    def addCategory(self, mainWinObj):
        newCategory = self.newCatEntry.get()
        catColor = self.changeColor['bg']
        mainWinObj.allAcc.categoriesColor[newCategory] = catColor
        StyleFormat.updateCategoryStyle(newCategory, catColor)
        listOfCategories = list(mainWinObj.allAcc.categoriesColor.keys())
        self.catListMenu.popupMenu.config(values = listOfCategories)

    def removeCategory(self, mainWinObj):
        # Check if any transaction is using the category
        delCategory = self.delListMenu.tkvar.get()
        mayDelete = True
        for iBankAcc in mainWinObj.allAcc.accountsObjs:
            for iTransaction in mainWinObj.allAcc.accountsObjs[iBankAcc].transactions:
                if mainWinObj.allAcc.accountsObjs[iBankAcc].transactions[iTransaction].category == delCategory:
                    mayDelete = False
        if mayDelete:
            del mainWinObj.allAcc.categoriesColor[delCategory]
            listOfCategories = list(mainWinObj.allAcc.categoriesColor.keys())
            self.catListMenu.popupMenu.config(values = listOfCategories)
            self.catListMenu.tkvar.set(listOfCategories[0])
            self.delListMenu.popupMenu.config(values = listOfCategories)
            self.delListMenu.tkvar.set(listOfCategories[0])

    def renameCategory(self, mainWinObj):
        prevName = self.renameListMenu.tkvar.get()
        newName = self.newCatNameEntry.get()
        catColor = mainWinObj.allAcc.categoriesColor[prevName]
        for iBankAcc in mainWinObj.allAcc.accountsObjs:
            for iTransaction in mainWinObj.allAcc.accountsObjs[iBankAcc].transactions:
                if mainWinObj.allAcc.accountsObjs[iBankAcc].transactions[iTransaction].category == prevName:
                    mainWinObj.allAcc.accountsObjs[iBankAcc].transactions[iTransaction].category = newName
            for iMonthYear in mainWinObj.allAcc.accountsObjs[iBankAcc].categoriesTotal:
                try:
                    mainWinObj.allAcc.accountsObjs[iBankAcc].categoriesTotal[iMonthYear][newName] = mainWinObj.allAcc.accountsObjs[iBankAcc].categoriesTotal[iMonthYear].pop(prevName)
                except:
                    pass

        mainWinObj.allAcc.categoriesColor[newName] = mainWinObj.allAcc.categoriesColor.pop(prevName)
        StyleFormat.updateCategoryStyle(newName, catColor)

        listOfCategories = list(mainWinObj.allAcc.categoriesColor.keys())
        self.renameListMenu.popupMenu.config(values = listOfCategories)
        self.renameListMenu.tkvar.set(listOfCategories[0])
        self.catListMenu.popupMenu.config(values = listOfCategories)
        self.catListMenu.tkvar.set(listOfCategories[0])
        self.delListMenu.popupMenu.config(values = listOfCategories)
        self.delListMenu.tkvar.set(listOfCategories[0])
        for iTransactionBoard in mainWinObj.accPage.transFrame.transContainer.transactions:
            mainWinObj.accPage.transFrame.transContainer.transactions[iTransactionBoard].UpdateBoard()

class OptionsButton(tk.Frame):
    #Class to create the dropdown menu
    def __init__(self, parent, choices, nrow, ncol, mainWinObj, currCatColor):
        if len(choices) == 0:
            choices.append("Sem Conta")
        # Create a Tkinter variable
        self.tkvar = tk.StringVar(parent)
        self.mainWinObj = mainWinObj
        self.currCatColor = currCatColor

        # Dictionary with options
        self.tkvar.set(choices[0]) # set the default option
    
        self.popupMenu = ttk.Combobox(parent, textvariable = self.tkvar, values = choices, state = 'readonly')
        #self.popupMenu.config(bd=0, bg="white")
        self.popupMenu.grid(row = nrow, column =ncol, sticky="nsew")
        
        # link function to change dropdown
        self.tkvar.trace('w', self.updWoutAsk)
    # on change dropdown value
    def updWoutAsk(self, *args):
        category = self.tkvar.get()
        color = self.mainWinObj.allAcc.categoriesColor[category]
        self.currCatColor.configure(bg = color)
