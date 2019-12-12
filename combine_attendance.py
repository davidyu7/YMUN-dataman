import csv
import cs50
import xlrd

with open("Committees.csv", "r") as committee_list: # use MDS
    reader = csv.DictReader(committee_list, delimiter=',')

    for row in reader:
        if row["Assignments Name"] == "2025: Arctic Council":
            comm_file_name = "2025_ Arctic Council.xlsx"
        elif row["Assignments Name"] == "Joint Crisis Committee (JCC): CIA":
            comm_file_name = "Joint Crisis Committee (JCC)_ CIA.xlsx"
        elif row["Assignments Name"] == "Joint Crisis Committee (JCC): KGB":
            comm_file_name = "Joint Crisis Committee (JCC)_ KGB.xlsx"
        elif row["Assignments Name"] == "Common Ministerial Council of the Austro-Hungarian Empire, July 1914":
            comm_file_name = "Common Ministerial Council of the Austro-Hungarian.xlsx"
        else:
            comm_file_name = row["Assignments Name"] + '.xlsx'
        if comm_file_name == "UNHCR.xlsx":
            with xlrd.open_workbook(comm_file_name) as wb:
                sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
                with open('Attendance.csv', 'w') as f:   # open('a_file.csv', 'w', newline="") for python 3
                    c = csv.writer(f)
                    for r in range(sh.nrows):
                        c.writerow(sh.row_values(r))
        else:
            with xlrd.open_workbook(comm_file_name) as wb:
                sh = wb.sheet_by_index(0)
                with open('Attendance.csv', 'a') as f:   # open('a_file.csv', 'w', newline="") for python 3
                    c = csv.writer(f)
                    for r in range(1, sh.nrows):
                        c.writerow(sh.row_values(r))


db = cs50.SQL("sqlite:///data_XLVI.db")

db.execute("DELETE FROM Attendance")

with open("Attendance.csv", "r") as delegates: # use project sheet (Delegates.csv)
    reader = csv.DictReader(delegates, delimiter=',')

    for row in reader:

        db.execute("INSERT INTO Attendance (name, school, s1, s2, s3, s4, s5, s6, s7) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
                       row["Name"], row["School"], row["Session 1"], row["Session 2"], row["Session 3"], row["Session 4"], row["Session 5"], row["Session 6"], row["Session 7"])

