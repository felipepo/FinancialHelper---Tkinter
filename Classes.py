import Funs
import re
import os,binascii

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
        self.transactions = {}
        self.categoriesTotal = {}

class Transaction:
    # Class to create a transaction using __slots__, which makes a class faster than a dictionary
    __slots__ = ('transID', 'category', 'value', 'date', 'comment', 'bankAccount', 'month', 'year')
    def __init__(self, transID, cat, val, date, com, acc):
        self.transID = transID
        self.category = cat
        self.value = val
        self.date = date
        self.comment = com
        self.bankAccount = acc
        self.month, self.year = Funs.GetMY(date)
    
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
            }

    def AddTransaction(self, category, value, date, comment, bankAccount,transID = "default"):
        datePattern = re.compile(r'[0-3]\d/[0-1]\d/\d{4}\Z')
        matched = datePattern.match(date)
        if not matched:
            return False
        else:
            try:
                self.accountsObjs[bankAccount].totalAmount += float(value)
                if transID == "default":
                    currTrans = binascii.b2a_hex(os.urandom(15))
                else:
                    currTrans = transID
                self.accountsObjs[bankAccount].transactions[currTrans] = Transaction(currTrans, category, value, date, comment, bankAccount)
                mon_year = self.accountsObjs[bankAccount].transactions[currTrans].month + "_" + self.accountsObjs[bankAccount].transactions[currTrans].year
                if mon_year in list(self.accountsObjs[bankAccount].categoriesTotal.keys()):
                    if category in list(self.accountsObjs[bankAccount].categoriesTotal[mon_year].keys()):
                        self.accountsObjs[bankAccount].categoriesTotal[mon_year][category] += float(value)
                    else:
                        self.accountsObjs[bankAccount].categoriesTotal[mon_year][category] = float(value)
                else:
                    self.accountsObjs[bankAccount].categoriesTotal[mon_year] = {}
                    self.accountsObjs[bankAccount].categoriesTotal[mon_year][category] = float(value)
                return currTrans
            except:
                return False
    
    def UpdateTransaction(self, currTrans, category, value, date, comment, bankAccount, prev_bankAccount):
        datePattern = re.compile(r'[0-3]\d/[0-1]\d/\d{4}\Z')
        matched = datePattern.match(date)
        if not matched:
            return False
        else:
            try:
                # Get previous Values
                prev_value = float(self.accountsObjs[prev_bankAccount].transactions[currTrans].value)
                prev_mon_year = self.accountsObjs[prev_bankAccount].transactions[currTrans].month + "_" + self.accountsObjs[prev_bankAccount].transactions[currTrans].year
                prev_category = self.accountsObjs[prev_bankAccount].transactions[currTrans].category

                # Update all the necessary parameters before assigning updated values
                self.accountsObjs[prev_bankAccount].totalAmount -= prev_value
                self.accountsObjs[prev_bankAccount].categoriesTotal[prev_mon_year][prev_category] -= float(prev_value)
                if self.accountsObjs[prev_bankAccount].categoriesTotal[prev_mon_year][prev_category] == 0:
                    del self.accountsObjs[prev_bankAccount].categoriesTotal[prev_mon_year][prev_category]
                    if not self.accountsObjs[prev_bankAccount].categoriesTotal[prev_mon_year]:
                        del self.accountsObjs[prev_bankAccount].categoriesTotal[prev_mon_year]
                
                # Assign updated values to target transaction object
                if bankAccount != prev_bankAccount:
                    self.AddTransaction(category, value, date, comment, bankAccount, currTrans)
                    del self.accountsObjs[prev_bankAccount].transactions[currTrans]
                else:
                    month, year = Funs.GetMY(date)
                    mon_year = month + "_" + year
                    self.accountsObjs[bankAccount].totalAmount += float(value)
                    self.accountsObjs[bankAccount].transactions[currTrans].comment = comment
                    self.accountsObjs[bankAccount].transactions[currTrans].bankAccount = bankAccount
                    self.accountsObjs[bankAccount].transactions[currTrans].year = year
                    self.accountsObjs[bankAccount].transactions[currTrans].month = month
                    self.accountsObjs[bankAccount].transactions[currTrans].category = category
                    self.accountsObjs[bankAccount].transactions[currTrans].value = value
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
if __name__ == "__main__":
    #Create all accounts
    allAcc = AllAccounts()

    #Add transaction when there is no accounts
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","BB")

    #Add Account
    allAcc.AddAcc("BB")
    #Add transaction to an account that doesn't exist
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")

    allAcc.AddAcc("Santander")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Feira",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Remédio",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Feira",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")
    allAcc.AddTransaction("Feira",50,"05/03/2015","BK","BB")
    allAcc.AddTransaction("Food",50,"05/03/2015","BK","Santander")


    #Check all accounts attributes
    print(allAcc.accountsObjs)
    #Funs.showdic(allAcc.transactions)
    print(allAcc.accountsObjs["BB"].transactions.keys())

    #Check specific accounts attributes
    print(allAcc.accountsObjs["BB"].totalAmount)
    #Funs.showdic(allAcc.accountsObjs["Santander"].transactions)
