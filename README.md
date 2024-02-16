<strong>
# creditCard

Credit card functions as follows: 
	• Each card has an APR and Credit Limit.
	• Interest is calculated daily, starting the day after the account is opened, at the close of each day.
	• Calculated interest becomes due at the close every 30 days after the account has been opened.
	• e.g., asking for the total outstanding balance 15, 28, or 29 days after opening will give the outstanding balance, but asking for balance 30 days after opening will give the outstanding balance plus the accrued interest.

To RUN:

1.)  docker pull aj82/python-appcc:ccapr

2.)  docker run -it aj82/python-appcc:ccapr python app.py -p $CMD
	
Replace $CMD with Login or SignUp
	
                OR 

1.) Setup a virtual environment

2.) PIP install pyrebase, argparse, google-cloud-firestore and firebase-admin

3.) Just install PyCharm IDE, open the folder does the above tasks automatically

4.) Run python app.py -p SignUp or Login

Sample User Login: m@m.com | password: test123

User Stories:
https://trello.com/b/8Gf4pgHA/task-credit-card

The software does the following:
	
	Create an account (e.g. opening a new credit card); Achieved using by making an FireBase account
	
	Keep track of charges (e.g. card swipes) 
	
	Keep track of payments
	
	Provide the total outstanding balance as of any given day
Next Steps:
 1.) Implement Try and Except
 2.) Unit Test


Built using Python and Firebase.

-> Firebase for authentication and Firestore database

Firebase authentication, lets the user create a/c. Firestore Database stores transactions, swipes, charges, payments.
Python Script processes everything above!!


Video Link: https://drive.google.com/open?id=1GaTnaqgYai_djEPMaLVxup6MAurzCcIa

Test Scenario 1
	• A customer opens a credit card with a $1,000.00 limit at a 35% APR.
	• The customer charges $500 on opening day (outstanding balance becomes $500).
	• The total outstanding balance owed 30 days after opening should be $514.38.
	• 500 * (0.35 / 365) * 30 = 14.38 
	
	
On 30th Day:


![30day](https://user-images.githubusercontent.com/30497847/54495153-55f35d80-48af-11e9-9561-30fc310772eb.PNG)


On 29th Day (before 30th day):


![29day](https://user-images.githubusercontent.com/30497847/54495162-715e6880-48af-11e9-8d13-eb4c5addfc13.PNG)

Test Scenario 2 
	• A customer opens a credit card with a $1,000.00 limit at a 35% APR.
	• The customer charges $500 on opening day (outstanding balance becomes $500).
	• 15 days after opening, the customer pays $200 (outstanding balance becomes $300).
	• 25 days after opening, the customer charges another $100 (outstanding balance becomes $400).
	• The total outstanding balance owed 30 days after opening should be $411.99.
	• (500 * 0.35 / 365 * 15) + (300 * 0.35 / 365 * 10) + (400 * 0.35 / 365 * 5) = 11.99
	
	
On 30th Day for single transaction in a month:


![1day](https://user-images.githubusercontent.com/30497847/54495175-86d39280-48af-11e9-9261-f7f2b2fa58b6.PNG)




</strong>

