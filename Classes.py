import Funs
import re

'''Classes related to the functioning of the program

    Account
    AllAccounts
    CreditCard
    Transaction
'''

class Account:
    #Class to create the accounts
    def __init__(self):
        self.name = None
        self.totalAmount = 0
        self.nextTrans = 0
        self.transactions = {}
        self.categoriesTotal = {}

class Transaction:
    # Class to create a transaction using __slots__, which makes a class faster than a dictionary
    __slots__ = ('category', 'value', 'date', 'comment', 'bankAccount', 'month', 'year')
    def __init__(self, cat, val, date, com, acc):
        month, year = Funs.GetMY(date)
        self.category = cat
        self.value = val
        self.date = date
        self.comment = com
        self.bankAccount = acc
        self.month = month
        self.year = year
    
#=========================================================================================
class AllAccounts():
    #Class to create an overall account
    def __init__(self):
        Account.__init__(self)
        self.accountsObjs = {}
        self.categoriesColor = {
            "Feira": 'navajo white',
            "Transporte": 'coral',
            "Remédio": 'hot pink',
            "Academia": 'violet red',
            "Aluguel": 'PaleGreen1',
            "Condomínio": 'DarkSlateGray1',
            "Telefone": 'khaki3',
            "Internet": 'LightGoldenrod1',
            "Luz": 'firebrick1',
            "Transporte": 'plum1',
            }

    def AddTransactiontoAll(self, category, value, date, comment, bankAccount):
        datePattern = re.compile(r'[0-3]\d/[0-1]\d/\d{4}\Z')
        matched = datePattern.match(date)
        if not matched:
            return False
        else:
            try:
                self.accountsObjs[bankAccount].totalAmount += float(value)
                self.totalAmount += float(value)
                currTrans = "trans"+str(self.accountsObjs[bankAccount].nextTrans)
                self.accountsObjs[bankAccount].transactions[currTrans] = Transaction(category, value, date, comment, bankAccount)
                self.accountsObjs[bankAccount].nextTrans += 1
                mon_year = self.accountsObjs[bankAccount].transactions[currTrans].month + "_" + self.accountsObjs[bankAccount].transactions[currTrans].year
                if mon_year in list(self.accountsObjs[bankAccount].categoriesTotal.keys()):
                    if category in list(self.accountsObjs[bankAccount].categoriesTotal[mon_year].keys()):
                        self.accountsObjs[bankAccount].categoriesTotal[mon_year][category] += float(value)
                    else:
                        self.accountsObjs[bankAccount].categoriesTotal[mon_year][category] = float(value)
                else:
                    self.accountsObjs[bankAccount].categoriesTotal[mon_year] = {}
                    self.accountsObjs[bankAccount].categoriesTotal[mon_year][category] = float(value)
                return True
            except:
                return False

    def AddAcc(self, accName):
        if accName in self.accountsObjs:
            return False #Didn't add a new account
        else:
            self.accountsObjs[accName] = Account()
            self.accountsObjs[accName].name = accName
            return True #Added a new account
        
    def DelAcc(self, accName):
        if accName in self.accountsObjs:
            del self.accountsObjs[accName]
            return True #Removed item from dictionary
        else:
            return False #Didn't removed item from dictionary

#=========================================================================================
class CreditCard(Account):
    #Class to create the credit cards accounts
    def __init__(self, ccName):
        self.limit = 0
'''
#Create all accounts
allAcc = AllAccounts()

#Add transaction when there is no accounts
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","BB")

#Add Account
allAcc.AddAcc("BB")
#Add transaction to an account that doesn't exist
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","Santander")

allAcc.AddAcc("Santander")
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","BB")
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","Santander")
allAcc.AddTransactiontoAll("Feira",50,"05/03/2015","BK","BB")
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","Santander")
allAcc.AddTransactiontoAll("Remédio",50,"05/03/2015","BK","BB")
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","Santander")
allAcc.AddTransactiontoAll("Feira",50,"05/03/2015","BK","BB")
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","Santander")
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","BB")
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","Santander")
allAcc.AddTransactiontoAll("Feira",50,"05/03/2015","BK","BB")
allAcc.AddTransactiontoAll("Food",50,"05/03/2015","BK","Santander")


#Check all accounts attributes
print(allAcc.accountsObjs)
print(allAcc.totalAmount)
#Funs.showdic(allAcc.transactions)

#Check specific accounts attributes
print(allAcc.accountsObjs["BB"].totalAmount)
#Funs.showdic(allAcc.accountsObjs["Santander"].transactions)'''
