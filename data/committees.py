import csv
import cs50
import sys

if(len(sys.argv) != 2):
    print("Usage: python code csv")
    sys.exit()

db = cs50.SQL("sqlite:///data_XLVI.db")

db.execute("DELETE FROM Committees")

with open(sys.argv[1], "r") as committees: # use Committee Info on Data Output Master (Committees.csv)
    reader = csv.DictReader(committees, delimiter=',')

    for row in reader:

        # combination_id = db.execute("SELECT name FROM Staffers WHERE committee = row['Name'];") # IS THERE A WAY TO DO THIS CORRECTLY? (for OH)

        db.execute("INSERT INTO Committees (id, organ, fullname, assignedname, capacity, size, day1, day2, day3, day4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                       row["ID"], row["Organ"], row["Name"], row["Assignments Name"], row["Capacity"], row["Current Size"], row["Day 1 Room"], row["Day 2 Room"],
                       row["Day 3 Room"], row["Day 4 Room"])