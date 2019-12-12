import csv
import cs50
import sys

if(len(sys.argv) != 2):
    print("Usage: python code csv")
    sys.exit()

db = cs50.SQL("sqlite:///data_XLVI.db")

db.execute("DELETE FROM Rooming")

with open(sys.argv[1], "r") as rooms: # use project sheet (Rooms.csv)
    reader = csv.DictReader(rooms, delimiter=',')

    for row in reader:

        db.execute("INSERT INTO Rooming (id, building, day1, day2, day3, day4) VALUES (?, ?, ?, ?, ?, ?);", row["Room ID"], row["Building"],
        row["Day1"], row["Day2"], row["Day3"], row["Day4"])