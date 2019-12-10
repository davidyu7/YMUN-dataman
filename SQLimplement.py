import cs50

db = cs50.SQL("sqlite:///data_XLVI.db")

# Drops existing tables (must be created already for this to work, otherwise cut out until created first time)

db.execute("DROP TABLE Attendance")
db.execute("DROP TABLE Committees")
db.execute("DROP TABLE Delegates")
db.execute("DROP TABLE Advisors")
db.execute("DROP TABLE Delegations")
db.execute("DROP TABLE Staffers")
db.execute("DROP TABLE Rooming")

# Creates tables

db.execute("CREATE TABLE IF NOT EXISTS Committees (id varchar, organ varchar, fullname text, assignedname text, capacity int, size int, day1 varchar, day2 varchar, day3 varchar, day4 varchar);") ##consider as table

db.execute("CREATE TABLE IF NOT EXISTS Delegates (id integer PRIMARY KEY, name varchar, school varchar, committee_assigned varchar, position_name varchar);")

db.execute("CREATE TABLE IF NOT EXISTS Advisors (id integer PRIMARY KEY, name varchar, point_of_contact bit NOT NULL DEFAULT(0), school varchar, email varchar, us_phone_number varchar);")

db.execute("CREATE TABLE IF NOT EXISTS Delegations (school_name varchar, d_i char, country varchar, delegate_count int, advisor_count int);") ##consider as table

db.execute("CREATE TABLE IF NOT EXISTS Staffers (id integer PRIMARY KEY, name varchar, position varchar, head_chair bit NOT NULL DEFAULT(0), committee_id varchar, email varchar, phone_number varchar);")

db.execute("CREATE TABLE IF NOT EXISTS Rooming (id varchar, building varchar, day1 varchar, day2 varchar, day3 varchar, day4 varchar);") ##consider as table

db.execute("CREATE TABLE IF NOT EXISTS Attendance (delegate_id int, s1 bit NOT NULL DEFAULT(0), s2 bit NOT NULL DEFAULT(0), s3 bit NOT NULL DEFAULT(0), s4 bit NOT NULL DEFAULT(0), s5 bit NOT NULL DEFAULT(0), s6 bit NOT NULL DEFAULT(0), s7 bit NOT NULL DEFAULT(0), FOREIGN KEY(id) REFERENCES Delegates(id));")