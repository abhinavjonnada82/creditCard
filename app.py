import pyrebase
import argparse
from abc import ABC, abstractmethod
import google.cloud
import firebase_admin
from firebase_admin import credentials,firestore



config = {
  "apiKey": "----------",
  "authDomain": "taskcc.firebaseapp.com",
  "databaseURL": "https://taskcc.firebaseio.com",
  "projectId": "taskcc",
  "storageBucket": "taskcc.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
cred = credentials.Certificate("./serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()



class CreditCard:
    def __init__(self):
        self.balance = 0
        print("Hello !! Welcome to your Checkings A/C")

    def deposit(self):
        amount = float(input("Enter amount to payed: "))
        self.balance += amount
        print("Amount Deposited {}".format(amount))

    def withdraw(self):
        amount = float(input("Enter amount to be Withdrawed: "))
        if self.balance >= amount:
            self.balance-= amount
            print(" You Withdrawed: {}".format(amount))
        else:
            print("Insufficient balance")

    def display(self):
        print("Net available balance {}".format(self.balance))

class CrudBase(ABC):
    def __init__(self, para):
        self.para = para

    def checkOptionEntered(self, para0, para1, para2):
        raise NotImplementedError("Subclass must implement this abstract method")

class CrudInAction(CrudBase):
    def __init__(self, f):
        super().__init__(f)

    def checkOptionEntered(self, actionOption, nameUser, user):

        if (actionOption == 'Make'):

            lis2 = []
            date = int(input("Enter only date (03/dd/2019): \n"))
            reason = input("Enter your expense: \n")
            price = int(input("Enter Price: $ \n"))
            # Query to get prices of transactions
            docs = store.collection(nameUser).document(u'total').get()
            tmpDict = (docs.to_dict())
            lis2.append(tmpDict['OutStanding'])
            b = sum(lis2) + price
            creditAvail = 1000 - b #update outstanding
            # setting credit limit to $ 400 for simplicity
            if creditAvail != 0:
                data = {
                    u'Date': date,
                    u'ExpenseType': reason,
                    u'ExpensePrice': price,
                    u'OutStanding': b
                }
                store.collection(nameUser).add(data)
                print("Transaction Successfull")
            else:
                print("Insufficient Funds!")

            # updating total value
            totData = {
                u'totVal':creditAvail,
                u'Date': date,
                u'OutStanding': b
            }

            store.collection(nameUser).document(u'total').set(totData)


        elif (actionOption == 'View'):
            dateEntry = int(input("Enter only date (03/dd/2019): \n"))
            if (dateEntry == 30):
                count = 0
                lis = []
                valIs = []
                docs = store.collection(nameUser).where(u'Flag', u'==',True).get()
                for doc in docs:
                    tmp = (doc.to_dict())
                    lis.append(tmp['Date'])
                docs = store.collection(nameUser).where(u'Flag', u'==', True).get()
                for doc2 in docs:
                    tmp1 = (doc2.to_dict())
                    x= tmp1['OutStanding']
                    y= tmp1['Date']
                    for i in range(len(lis)):
                        if i == 0 and lis[i] == y:
                            if len(lis) == 1:
                                t = x * (0.35/365) * (30)
                                valIs.append(t)
                                break
                            else:
                                t = x * (0.35 / 365) * (30-lis[i+1])
                                valIs.append(t)
                                break
                        elif i == len(lis)-1 and lis[i] == y:
                            t = x * (0.35 / 365) * (30 - lis[i])
                            valIs.append(t)
                            break
                        elif lis[i] == y:
                            t = x * (0.35 / 365) * (lis[i+1]-lis[i])
                            valIs.append(t)
                            break

                docTot = store.collection(nameUser).document(u'total').get()
                tmpDict = (docTot.to_dict())
                outBal = tmpDict['OutStanding']
                print("Intrest at end of 30th day is $ {}".format(sum(valIs) + outBal))
            else:
                docs1 = store.collection(nameUser).document(u'total').get()
                tmpDict = (docs1.to_dict())
                outBal = tmpDict['OutStanding']
                print("Intrest on {} March 2019 is $ {}".format(dateEntry, outBal))


        elif (actionOption == 'Pay'):
            lis2 = []
            date = int(input("Enter only date (03/dd/2019): \n"))
            payment = int(input("Enter amount to be payed: $ \n"))
            docs = store.collection(nameUser).where(u'ExpensePrice', u'>=', 0).get()
            for doc in docs:
                tmpDict = (doc.to_dict())
                lis2.append(tmpDict['ExpensePrice'])
            b = sum(lis2) - payment  # update outstanding

            data = {
                u'Date': date,
                u'Payment': payment,
                u'OutStanding': b
            }
            store.collection(nameUser).add(data)
            print("Transaction Successfull")
            print("Outstanding balance $ {}".format(b))
            docTot = store.collection(nameUser).document(u'total')
            currentTotal = 1000 - b
            docTot.update({u'totVal': currentTotal, u'Date': date, u'OutStanding': b})
            print("Your available credit is $ {}".format(currentTotal))



# bridge function
def openBridge(user):
    if user:
        value = auth.get_account_info(user['idToken'])
        temp = value['users'][0]['email']
        tmp = temp.split('@')
        nameUser = tmp[0]

    print("""1.) Make Transactions: Make 2.) Pay your bill: Pay
                      3.) View your overall expenses: View 5.) Exit application: Logout """)
    actionOption = input("Enter your choice of entry: ")

    crud = CrudInAction("crud")
    crud.checkOptionEntered(actionOption, nameUser, user)

 # Create Credit Card
#
# def createCC(self):
#     n = 16
#     range_start = 10 ** (n - 1)
#     range_end = (10 ** n) - 1
#     return randint(range_start, range_end)




# base class

class BaseMenu(ABC):
    def __init__(self, par):
        self.par = par

    @abstractmethod
    def emailEntry(self):
        raise NotImplementedError("Subclass must implement this abstract method")

    @abstractmethod
    def passwordEntry(self):
        raise NotImplementedError("Subclass must implement this abstract method")

    @abstractmethod
    def menuHandler(self, f):
        raise NotImplementedError("Subclass must implement this abstract method")

# derived class

class MenuHandlerAction(BaseMenu):
    def __init__(self, f):
        super().__init__(f)

    # takes user input
    def emailEntry(self):
        print(" Welcome to Imperial Banking Life ")
        email = input("Please enter your email: \n")
        return email

    def passwordEntry(self):
        password = input("Please enter your password: \n")
        return password



    # based on user entry performs suitable authentication
    def menuHandler(self, optionsList):
        optionsHolder = optionsList.pop(0)

        if (optionsHolder == "Login"):
            email = self.emailEntry()
            password = self.passwordEntry()
            user = auth.sign_in_with_email_and_password(email, password)
            print ('Login Successful')
            openBridge(user)


        elif (optionsHolder == "SignUp"):

                email = self.emailEntry()
                password = self.passwordEntry()
                print ("Creating a new account!")
                print ('Account Created')
                user = auth.create_user_with_email_and_password(email, password)
                print('SignUp Successful')
                openBridge(user)


        elif (optionsHolder == "ForgotPassword"):
            try:
                email = input("Please enter your email \n")
                user = auth.send_password_reset_email(email)
                print("Check your email!")
            except:
                print('Wrong email, please check your credentials!')


if __name__ == "__main__":

# argparse module lets you add options upon first entry

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest="optionsAvail", nargs='*',
                        help='''Options available: 1.) Login 2.) SignUp
                            3.) Forgot Password''')

    args = parser.parse_args()
    optionsList = args.optionsAvail
    menu = MenuHandlerAction("menu")
    menu.menuHandler(optionsList)
