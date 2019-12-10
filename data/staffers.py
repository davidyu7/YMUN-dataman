import csv
import cs50
import sys

if(len(sys.argv) != 2):
    print("Usage: python code csv")
    sys.exit()

db = cs50.SQL("sqlite:///data_XLVI.db")

db.execute("DELETE FROM Staffers")

with open(sys.argv[1], "r") as staff: # use Master Staff List (Staff.csv)
    reader = csv.DictReader(staff, delimiter=',')

    for row in reader:

        db.execute("INSERT INTO Staffers (name, position, head_chair, committee_id, email, phone_number) VALUES (?, ?, ?, ?, ?, ?);",
                       row["Name"], row["Position"], row["Head?"], row["ID"], row["Email"], row["Phone"])