<strong>
# creditCard

Credit card functions as follows: 
	• Each card has an APR and Credit Limit.
	• Interest is calculated daily, starting the day after the account is opened, at the close of each day.
	• Calculated interest becomes due at the close every 30 days after the account has been opened.
	• e.g., asking for the total outstanding balance 15, 28, or 29 days after opening will give the outstanding balance, but asking for balance 30 days after opening will give the outstanding balance plus the accrued interest.

The software does the following:
	Create an account (e.g. opening a new credit card)
	Keep track of charges (e.g. card swipes)
	Keep track of payments
	Provide the total outstanding balance as of any given day

Built using Python and Firebase.
-> ArgParse, Firebase admin and Pyrebase modules
-> Firebase for authentication and database

1.) Setup a virtual environment
2.) PIP install pyrebase, argparse, google-cloud-firestore and firebase-admin
3.) Just install PyCharm IDE, open the folder does the above tasks automatically
4.) Run python app.py -p SignUp or Login

Sample User Login: m@m.com | password: test123

</strong>
