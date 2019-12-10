import os
import string

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

db = SQL("sqlite:///data_XLVI.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
def index():

    return render_template('homepage.html')

# Display the list of all committees
@app.route("/committees", methods=["GET"])
def displayCommittees():

    if request.method =="GET":

        # Select information about all the committees, as well as the head chair for each committee
        committees = db.execute("SELECT Committees.*, Staffers.name FROM Committees JOIN Staffers ON Committees.id = Staffers.committee_id WHERE Staffers.head_chair = '1';")

        #debug print(committees)

        # Render the page
        return render_template('committees.html', committees=committees)

# Individual Committee Information Page
@app.route("/display-committee", methods=["GET", "POST"])
def displayCommitteeInfo():

    # The user has requested to see information about a specific committee
    if request.method == "GET":

        # get committee ID from GET request parameter
        committee_id=request.args.get('committee_id')

        #debug print(committee_id)

        # Select info about the requested committee
        committee = db.execute("SELECT * FROM Committees WHERE id = ?;", committee_id)[0]

        # Select info about staffers
        staffers = db.execute("SELECT * FROM Staffers WHERE committee_id = ?;", committee_id)

        # Select the list of delegates in the requested committee, using the "assignedname" used in position sheets that were sent to advisors
        delegates = db.execute("SELECT * FROM Delegates WHERE committee_assigned = ?", committee["assignedname"])

        #debug print(committee)

        # Render the page
        return render_template('display-committee.html', delegates=delegates, committee_id=committee_id, committee=committee, staffers=staffers)

# Display the list of all delegations
@app.route("/delegations", methods=["GET"])
def displayDelegations():

    if request.method =="GET":

        # Select information about all the delegations, as well as the point of contact advisor for each delegation
        delegations = db.execute("SELECT * FROM Delegations JOIN Advisors ON Delegations.school_name = Advisors.school WHERE Advisors.point_of_contact = '1' ORDER BY school_name;")

        #debug print(delegations)

        # Render the page
        return render_template('delegations.html', delegations=delegations)

# Individual Delegation Information Page
@app.route("/display-delegation", methods=["GET", "POST"])
def displayDelegationInfo():

    # The user has requested to see information about a specific delegation
    if request.method == "GET":

        # get delegation school name from GET request parameter
        school_name = request.args.get('school_name')

        # Select info about the requested delegation, as well as the point of contact advisor for the delegation
        delegation = db.execute("SELECT * FROM Delegations JOIN Advisors ON Delegations.school_name = Advisors.school WHERE Advisors.point_of_contact = '1' AND school_name = ?;", school_name)[0]

        # Select info about advisors
        advisors = db.execute("SELECT * FROM Advisors WHERE school = ?;", school_name)

        # Select the list of delegates in the requested delegation, as well as the full name and internal abbreviation of the committee that they are in
        delegates = db.execute("SELECT Delegates.*, Committees.id as committee_id, Committees.fullname as committee_name FROM Delegates JOIN Committees ON Delegates.committee_assigned = committees.assignedname WHERE school = ?", school_name)

        print(delegates)

        # Render the page
        return render_template('display-delegation.html', delegates=delegates, school_name=school_name, delegation=delegation, advisors=advisors)

#Display the list of rooms
@app.route("/rooming", methods=["GET"])
def displayRooms():
    
    if request.method =="GET":
        
        #The requested room is not specified
        if not request.args.get('building')
        rooms = db.execute("SELECT * FROM Rooming;")

        return render_template('rooming.html')

@app.route("/absences", methods=["GET"])
def displayAbsences():
    if request.method =="GET":

        return render_template('absences.html')

@app.route("/s1", methods=["GET"])
def s1():
    if request.method =="GET":
        s1 = db.execute("SELECT * FROM Attendance;")

        return render_template('s1.html')

@app.route("/s2", methods=["GET"])
def s2():
    if request.method =="GET":
        s2 = db.execute("SELECT * FROM Attendance;")

        return render_template('s2.html')

@app.route("/s3", methods=["GET"])
def s3():
    if request.method =="GET":
        s3 = db.execute("SELECT * FROM Attendance;")

        return render_template('s3.html')

@app.route("/s4", methods=["GET"])
def s4():
    if request.method =="GET":
        s4 = db.execute("SELECT * FROM Attendance;")

        return render_template('s4.html')

@app.route("/s5", methods=["GET"])
def s5():
    if request.method =="GET":
        s5 = db.execute("SELECT * FROM Attendance;")

        return render_template('s5.html')

@app.route("/s6", methods=["GET"])
def s6():
    if request.method =="GET":
        s6 = db.execute("SELECT * FROM Attendance;")

        return render_template('s6.html')

@app.route("/s7", methods=["GET"])
def s7():
    if request.method =="GET":
        s7 = db.execute("SELECT * FROM Attendance;")

        return render_template('s7.html')
        
