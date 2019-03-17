import pyrebase
import argparse
from abc import ABC, abstractmethod
import google.cloud
import firebase_admin
from firebase_admin import credentials,firestore
import sys



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

class HelperBase():
    def __init__(self, para):
        self.para = para

    #helper functions

    def responseHolderfun(self, actionOption, nameUser, user):
        responseHolder = input("Do you want to {} once more? Y/N ".format(actionOption))
        while True:
            if (responseHolder == ('Y' or 'y')):
                action1 = ActionCenter("action1")
                action1.checkOptionEntered(actionOption, nameUser, user)
            else:
                break
        openBridge(user)

    def queryTotalDoc(self, nameUser):
        # Query for total Document
        docs = store.collection(nameUser).document(u'total')
        return docs

    def queryAutoIDDoc(self, nameUser):
        # Query for Document with AutoID
        docs = store.collection(nameUser)
        return docs

    # Loops over AutoID query and returns a dictionary
    def loopOverAutoID(self, nameUser):
        docs = self.queryAutoIDDoc(nameUser).where(u'Flag', u'==', True).get()
        for doc in docs:
            tmp = (doc.to_dict())
        return tmp

    # prints outstanding balance
    def printInterest(self, nameUser):
        docTot = store.collection(nameUser).document(u'total').get()
        tmpDict = (docTot.to_dict())
        outBal = tmpDict['OutStanding']
        return outBal

class ActionBase(ABC):
    def __init__(self, para):
        self.para = para


    def checkOptionEntered(self, para0, para1, para2):
        raise NotImplementedError("Subclass must implement this abstract method")

class ActionCenter(ActionBase):
    def __init__(self, f):
        super().__init__(f)

    def checkOptionEntered(self, actionOption, nameUser, user):
        holder = HelperBase("holder")


# User makes a transaction by manually entering data
        if (actionOption == 'Make'):

            lis2 = [] # list to hold outstanding balance!!
            date = int(input("Enter only date (03/dd/2019): \n"))
            reason = input("Enter your expense: \n")
            price = int(input("Enter Price: $ \n"))

            # Query to get outstanding balance of current transactions
            docs = holder.queryTotalDoc(nameUser).get()
            # converting object to dictionary and using key value pairs to get OutStanding bal.
            tmpDict = (docs.to_dict())
            if tmpDict == None:
                lis2.append(0)
            else:
                lis2.append(tmpDict['OutStanding'])
            b = sum(lis2) + price # current outstanding balance
            creditAvail = 1000 - b # updated credit limit
            # setting credit limit to $ 1000 for simplicity and makin sure user transactions are limited to $1000
            if creditAvail != 0:
                data = {
                    u'Date': date,
                    u'ExpenseType': reason,
                    u'ExpensePrice': price,
                    u'OutStanding': b,
                    u'totVal': creditAvail,
                    u'Flag': True
                }
                # Query for Document with AutoID
                holder.queryAutoIDDoc(nameUser).add(data)
                print("Transaction Successfull")
            else:
                print("Insufficient Funds!")

            # updating total value
            totData = {
                u'totVal':creditAvail,
                u'Date': date,
                u'OutStanding': b
            }
            # query to update values using queryTotalDoc method
            holder.queryTotalDoc(nameUser).set(totData)
            # method call to know if user wants perform same action again
            holder.responseHolderfun(actionOption, nameUser, user)


        # if (actionOption == 'View'):
        #     dateEntry = int(input("Enter only date (03/dd/2019): \n"))
        #     if (dateEntry == 30):
        #     # if clause on 30th day
        #         dataLis = [] # to hold list of transaction dates
        #         interestAcc = [] # holds accured interest for transaction
        #     # Loops over AutoID query and returns a dictionary
        #     docs = store.collection(nameUser).where(u'Flag', u'==', True).get()
        #     for doc in docs:
        #         tmp = (doc.to_dict())
        #         dataLis.append(tmp['Date'])
        #     # updates dataLis
        #         print(dataLis)
        #         #tmp1 = holder.loopOverAutoID(nameUser) # method call to loop over below query
        #     # calls in a query to get Outstanding balance and date from each transaction
        #         docs = store.collection(nameUser).where(u'Flag', u'==', True).get()
        #         for doc2 in docs:
        #             tmp1 = (doc2.to_dict())
        #             x= tmp1['OutStanding']
        #             y= tmp1['Date']
        #             print(x, y)
        #             for i in range(len(dataLis)):
        #                 # loops over dataLis to calculate interest rate for each transaction
        #                 if i == 0 and dataLis[i] == y: # checks index position and compares date form the
        #                     # dataLis and query above
        #
        #                     if len(dataLis) == 1: # for only single transactions in a month
        #                         t = x * (0.35/365) * (30)
        #                         interestAcc.append(t)
        #                         break
        #                     else: # first transaction in a month
        #                         t = x * (0.35 / 365) * (30-dataLis[i+1])
        #                         interestAcc.append(t)
        #                         break
        #                 # for last transactions
        #                 elif i == len(dataLis)-1 and dataLis[i] == y:
        #                     t = x * (0.35 / 365) * (30 - dataLis[i])
        #                     interestAcc.append(t)
        #                     break
        #                 # for transactions inbetween months
        #                 elif dataLis[i] == y:
        #                     t = x * (0.35 / 365) * (dataLis[i+1]-dataLis[i])
        #                     interestAcc.append(t)
        #                     break
        #             print(interestAcc)
        #
        #         outBalance = holder.printInterest(nameUser)
        #         print("Intrest at end of 30th day is $ {}".format(sum(interestAcc) + outBalance))
        #
        #     else:
        #         outBalance = holder.printInterest(nameUser)
        #         print("Intrest on {} March 2019 is $ {}".format(dateEntry, outBalance))
        #
        #     holder = HelperBase("holder")
        #     holder.responseHolderfun(actionOption, nameUser, user)
    # issue with above view function!!, had to implement bottom!!

        if (actionOption == 'View'):
            dateEntry = int(input("Enter only date (03/dd/2019): \n"))
            if (dateEntry == 30):
                count = 0
                lis = []
                valIs = []
                docs = store.collection(nameUser).where(u'Flag', u'==', True).get()
                for doc in docs:
                    tmp = (doc.to_dict())
                    lis.append(tmp['Date'])
                lis = sorted(lis)
                docs = store.collection(nameUser).where(u'Flag', u'==', True).get()
                for doc2 in docs:
                    tmp1 = (doc2.to_dict())
                    x = tmp1['OutStanding']
                    y = tmp1['Date']
                    for i in range(len(lis)):
                        if i == 0 and lis[i] == y:
                            if len(lis) == 1:
                                t = x * (0.35 / 365) * (30)
                                valIs.append(t)
                                break
                            else:
                                t = x * (0.35 / 365) * (30 - lis[i + 1])
                                valIs.append(t)
                                break
                        elif i == len(lis) - 1 and lis[i] == y:
                            t = x * (0.35 / 365) * (30 - lis[i])
                            valIs.append(t)
                            break
                        elif lis[i] == y:
                            t = x * (0.35 / 365) * (lis[i + 1] - lis[i])
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

        if (actionOption == 'Pay'):
            # for better contrast, I have directly used queries, instead of helper functions
            lis2 = [] # holds outstanding value
            date = int(input("Enter only date (03/dd/2019): \n"))
            payment = int(input("Enter amount to be payed: $ \n"))
            # query returns outStanding balance from total document and reutrns updated balance
            docs = store.collection(nameUser).document(u'total').get()
            tmpDict = (docs.to_dict())
            lis2.append(tmpDict['OutStanding'])
            b = sum(lis2) - payment  # update outstanding

            data = {
                u'Date': date,
                u'Payment': payment,
                u'OutStanding': b,
                u'Flag': True
            }
            # query adds a transaction
            store.collection(nameUser).add(data)
            print("Transaction Successfull")
            print("Outstanding balance $ {}".format(b))

            # query updates total document
            docTot = store.collection(nameUser).document(u'total')
            currentTotal = 1000 - b
            docTot.update({u'totVal': currentTotal, u'Date': date, u'OutStanding': b})
            print("Your available credit is $ {}".format(currentTotal))

            holder = HelperBase("holder")
            holder.responseHolderfun(actionOption, nameUser, user)

        # EXIT
        if (actionOption == 'Logout'):
            print("Bye....... see you soon! :) ")
            sys.exit()



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

    action = ActionCenter("action")
    action.checkOptionEntered(actionOption, nameUser, user)

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
# object
    menu = MenuHandlerAction("menu")
    menu.menuHandler(optionsList)