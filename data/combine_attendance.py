import csv
import cs50

with open("Attendances1.csv", "w") as attendance:
    attendance_writer = csv.writer(attendance, delimiter=',')

    with open("UNHCR - s1.csv", "r") as UNHCR:
        reader = csv.DictReader(UNHCR, delimiter=',')

        for row in reader:
            attendance_writer.writerow[row["School"], row["Name"], row["If present mark 1 otherwise mark 0"]

    UNHCR.close()
attendance.close()


import xlrd
import csv

with xlrd.open_workbook(committee_name[i]'.xls') as individual:
    attendance = individual.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
    with open('a_file.csv', 'wb') as f:   # open('a_file.csv', 'w', newline="") for python 3
        completed_attendance = csv.writer(f)
        for row in range(attendance.nrows):
            completed_attendance.writerow(attendance.row_values(r))

