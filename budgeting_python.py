"""
Connects to a SQL database using mssql-python

Important:
cursor = conn.cursor()
cursor.execute(SQL_QUERY)
"""

from os import getenv
from dotenv import load_dotenv
from mssql_python import connect

load_dotenv()
conn = connect(getenv("SQL_CONNECTION_STRING"))

cursor = conn.cursor()


"""
The Code
"""

import datetime
import sys

#This is the introduction to the program
print("!!! A T T E N T I O N !!! \nThe following program is designed according to the whims and ideals of Ryann. \nAny questions and concerns are to be directed to her!\nThis is a program designed to help you divide your money and spend it more mindfully.\nYou'll need to update it weekly to keep data consistent!")

choice1 = input("\n\nHello there! Thank you for choosing to use this program. \nDo you have an account? \n[Y/N]: ")

if choice1.upper() == 'Y':
    account_name = input("Enter account name: ")
    cursor.execute("SELECT * FROM "+account_name)
    data = cursor.fetchall()
    for i in data:
        print(i)

elif choice1.upper() == 'N':
    print("Let's start with creating an account.")
#Here start all the variables and data that will be collected and calculated
    account_name = input("Enter your name. This will be your account name: ")
    income = str(float(input("Enter your income this week: ")))
    rent = str(float(input("Enter your rent per week: ")))
    remaining1 = str(float(income)-float(rent))
    savings = str(0.2*float(remaining1))
    remaining2 = str(float(income)-float(rent)-float(savings))
    grocery_allowance = str(0.7*float(remaining2))
    grocery_spent = str(0)
    spending_allowance = str(0.3*float(remaining2))
    spending_spent = str(0)
    emergency_spending = str(0)
#SQL queries incoming!!!
    cursor.execute("INSERT INTO users VALUES('"+account_name+"',"+income+","+rent+")")
    conn.commit()
    cursor.execute("CREATE TABLE "+account_name+" (date_of_entry date,income float,rent float,savings float,grocery_allowance float,grocery_spent float,spending_allowance float,spending_spent float,emergency_spending float)")
    conn.commit()    
    cursor.execute("INSERT INTO "+account_name+" VALUES (CURRENT_DATE,"+income+","+rent+","+savings+","+grocery_allowance+","+grocery_spent+","+spending_allowance+","+spending_spent+","+emergency_spending+")")
    conn.commit()
    cursor.execute("SELECT * FROM "+account_name)
    data = cursor.fetchall()
    print(data)

    
else:
    sys.exit("Hmm, there seems to be a typo...")
    
choice2 = int(input("\n\nWhat needs to be done today?: \n[1] Make a new entry \n[2] Check my savings balance \n[3] Check my groceries allowance \n[4] Check my spending allowance \n[5] Check all my account details \n[6] EXIT \nEnter: "))
if choice2 == 1:
    old_date = str(input("Enter the last date of entry: "))
    old_date_1 =f"'{old_date}'"
    income = str(float(input("Enter this week's income: ")))
    rent = str(float(input("Enter this week's rent: ")))
    remaining1 = str(float(income) - float(rent))
    cursor.execute("SELECT savings FROM "+account_name+" WHERE date_of_entry = "+old_date_1)
    data = cursor.fetchall()
    for i in data:
        for j in i:
            savings_week_before = j
    savings = str(0.2*float(remaining1) + float(savings_week_before))
    remaining2 = str(float(income) - float(rent) - float(savings))
    cursor.execute("SELECT grocery_allowance-grocery_spent FROM "+account_name+" WHERE date_of_entry = "+old_date_1)
    data = cursor.fetchall()
    for i in data:
        for j in i:
            grocery_saved_week_before = j
    grocery_allowance = str(0.7*float(remaining2) + float(grocery_saved_week_before))
    grocery_spent = str(float(input("Enter this week's grocery spending: ")))
    cursor.execute("SELECT spending_allowance-spending_spent FROM "+account_name+" WHERE date_of_entry = "+old_date_1)
    data = cursor.fetchall()
    for i in data:
        for j in i:
            spending_saved_week_before = j
    spending_allowance = str(0.3*float(remaining2) + float(spending_saved_week_before))
    spending_spent = str(float(input("Enter this week's personal spending: ")))
    emergency_spending = str(float(input("Enter any spending from savings? (aka emergency spending, not out of your allowance): ")))
    cursor.execute("INSERT INTO "+account_name+" VALUES (CURRENT_DATE,"+income+","+rent+","+savings+","+grocery_allowance+","+grocery_spent+","+spending_allowance+","+spending_spent+","+emergency_spending+")")
    conn.commit()
    account_name_1 = f"'{account_name}'"
    cursor.execute("UPDATE users SET income = "+income+" where account_name = "+account_name_1)
    conn.commit()
elif choice2 == 2:
    cursor.execute("SELECT savings,grocery_allowance-grocery_spent as grocery_saved,spending_allowance-spending_spent as spending_saved FROM "+account_name+" WHERE date_of_entry = (SELECT max(date_of_entry) FROM "+account_name+")")
    data = cursor.fetchall()
    for i in data:
        print(i)
elif choice2 == 3:
    cursor.execute("SELECT grocery_allowance FROM "+account_name+" WHERE date_of_entry = (SELECT max(date_of_entry) FROM "+account_name+")")
    data = cursor.fetchall()
    for i in data:
        print(i)
elif choice2 == 4:
    cursor.execute("SELECT spending_allowance FROM "+account_name+" WHERE date_of_entry = (SELECT max(date_of_entry) FROM "+account_name+")")
    data = cursor.fetchall()
    for i in data:
        print(i)
elif choice2 == 5:
    cursor.execute("SELECT * FROM "+account_name)
    data = cursor.fetchall()
    for i in data:
        print(i)
elif choice2 == 6:
    sys.exit("\n\nThank you for using our services!!! \nSincerely, a bored 19 year old.")
else:
    sys.exit("what...???")
