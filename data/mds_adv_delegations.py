import csv
import cs50
import sys

if(len(sys.argv) < 2):
    print("Usage: python code csv")
    sys.exit()

db = cs50.SQL("sqlite:///data_XLVI.db")

db.execute("DELETE FROM Delegations")
db.execute("DELETE FROM Advisors")

with open(sys.argv[1], "r") as mds: # use MDS
    mds_reader = csv.DictReader(mds, delimiter=',')

    for row in mds_reader:

        advisor_name = row["Advisor First Name"] + ' ' + row["Advisor Last Name"]

        db.execute("INSERT INTO Advisors (name, point_of_contact, school, email, us_phone_number) VALUES (?, ?, ?, ?, ?);",
                       advisor_name, 1, row["Delegation Name"], row["Email"], row["Phone"])

        db.execute("INSERT INTO Delegations (school_name, country, d_i, delegate_count, advisor_count) VALUES (?, ?, ?, ?, ?);",
                        row["Delegation Name"], row["Country"], row["D/I"], row["# Students"], row["# Advisors"])

# Code in information for the remaining advisors!