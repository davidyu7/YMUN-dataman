import csv
import cs50
import sys

if(len(sys.argv) != 2):
    print("Usage: python code csv")
    sys.exit()

db = cs50.SQL("sqlite:///data_XLVI.db")

db.execute("DELETE FROM Delegates")

with open(sys.argv[1], "r") as delegates: # use project sheet (Delegates.csv)
    reader = csv.DictReader(delegates, delimiter=',')

    for row in reader:

        db.execute("INSERT INTO Delegates (name, school, committee_assigned, position_name) VALUES (?, ?, ?, ?);",
                       row["Name"], row["School"], row["Committee"], row["Position"])