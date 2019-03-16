import pyrebase
import argparse
from abc import ABC, abstractmethod
import google.cloud
import firebase_admin
from firebase_admin import credentials,firestore
from random import randint


config = {
  "apiKey": "AIzaSyAmkl4n9DuY5cTAUVKlZwomKQyIV3BY7Ms",
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

# bridge function
def openBridge(user, ccNum):
    if user and ccNum == 1:
        value = auth.get_account_info(user['idToken'])
        temp = value['users'][0]['email']
        tmp = temp.split('@')
        nameUser = tmp[0]
        # can be improved
        doc_ref = store.collection(nameUser).get()
        for doc in doc_ref:
            print(u'Doc Data:{}'.format(doc.to_dict()))

        print("Hello {}".format(nameUser))

    elif user and ccNum == 0:
        value = auth.get_account_info(user['idToken'])
        temp = value['users'][0]['email']
        tmp = temp.split('@')
        nameUser = tmp[0]
        # can be improved
        print("Hello {}".format(nameUser))
        valCC = createCC()
        print(valCC)
        doc_ref = store.collection(nameUser).document(str(ccNum))

    try:
        docs = doc_ref.get()
        for doc in docs:
            print(u'Doc Data:{}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')

    print("""1.) Make Transactions 2.) Pay your bill: Pay
                      3.) View your overall expenses: View 5.) Exit application: Logout """)
    actionOption = input("Enter your choice of entry: ")
    crud = CrudInAction("crud")
    crud.checkOptionEntered(actionOption, nameUser, user)

        # Create Credit Card

def createCC(self):
    n = 16
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)




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
            ccNum = 1
            openBridge(user, ccNum)


        elif (optionsHolder == "SignUp"):
            email = self.emailEntry()
            password = self.passwordEntry()

            print ("Creating a new account!")
            print ('Account Created')
            print("You're new credit card: ")
            ccNum = 0
            user = auth.create_user_with_email_and_password(email, password)
            openBridge(user, ccNum)


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