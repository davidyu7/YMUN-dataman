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

# Old database
# db = SQL("sqlite:///data_XLVI.db")

# New Heroku Database
db = SQL("postgres://hnqodbzrirphml:8c61d75015387e2141ba3db8d6072b730a4cc194646e09239f79226fc02f879a@ec2-174-129-255-37.compute-1.amazonaws.com:5432/ddlp8u4p34upr4")

@app.route("/", methods=["GET", "POST"])
def index():

    return render_template('index.html')

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
        if not request.args.get('building'):
            rooms = db.execute("SELECT * FROM Rooming JOIN Committees ON Committees.")

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


@app.route("/s7", methods=["GET"])
def s7():
    if request.method =="GET":
        s7 = db.execute("SELECT * FROM Attendance;")

        return render_template('s7.html')
# Display search results
@app.route("/results", methods=["GET"])
def search():

    # Determine whether the user wants to search through all tables or a specific one
    search_in = request.args.get("search_in")

    # Get the query from the http request
    query = "%" + request.args.get("query") + "%"

    # Initialize the results to an empty list
    results = []

    # Populate the results list with matches from the advisors table
    if search_in in ("advisors", "all"):

        # Format the matching advisors in a dictionary, adding information for the HTML template and headers
        result = {
            "type": "Advisors",
            "headers": ["Advisor Name", "School", "Phone", "Email"],
            "content": db.execute("SELECT name, school, us_phone_number, email FROM Advisors WHERE name LIKE ?;", query),
            "empty": False
        }

        # Update the dictionary field to "empty" if the search returned no results
        if result["content"] == []:
            result["empty"] = True

        # Add this result to the total results list
        results.append(result)

    # Populate the results list with matches from the delegates table
    if search_in in ("delegates", "all"):

        # Format the matching delegates in a dictionary, adding information for the HTML template and headers
        result = {
            "type": "Delegates",
            "headers": ["Delegate Name", "School", "Committee", "Position"],
            "content": db.execute("SELECT name, school, Committees.id AS committee_id, position_name FROM Delegates JOIN Committees ON Delegates.committee_assigned = Committees.assignedname WHERE name LIKE ?", query),
            "empty": False
        }

        # Update the dictionary field to "empty" if the search returned no results
        if result["content"] == []:
            result["empty"] = True

        # Add this result to the total results list
        results.append(result)

    # Populate the results list with matches from the delegations table
    if search_in in ("delegations", "all"):

        # Format the matching delegations in a dictionary, adding information for the HTML template and headers
        result = {
            "type": "Delegations",
            "headers": ["Delegation Name", "Country", "# Delegates", "# Advisors"],
            "content": db.execute("SELECT school_name AS school, country, delegate_count, advisor_count FROM Delegations WHERE school_name LIKE ?;", query),
            "empty": False
        }

        # Update the dictionary field to "empty" if the search returned no results
        if result["content"] == []:
            result["empty"] = True

        # Add this result to the total results list
        results.append(result)

    # Populate the results list with matches from the committees table
    if search_in in ("committees", "all"):

        # Format the matching committees in a dictionary, adding information for the HTML template and headers
        result = {
            "type": "Committees",
            "headers": ["ID", "Name", "# Delegates", "Head Chair", "Phone Number", "Email"],
            "content": db.execute("SELECT Committees.id AS committee_id, fullname, size, name, phone_number, email FROM Committees JOIN Staffers ON Committees.id = Staffers.committee_id WHERE Staffers.head_chair = '1' AND Committees.fullname LIKE ?;", query),
            "empty": False
        }

        # Update the dictionary field to "empty" if the search returned no results
        if result["content"] == []:
            result["empty"] = True

        # Add this result to the total results list
        results.append(result)

    # Populate the results list with matches from the staffers table
    if search_in in ("staffers", "all"):

        # Format the matching staffers in a dictionary, adding information for the HTML template and headers
        result = {
            "type": "Staffers",
            "headers": ["Name", "Position", "Committee", "Head Chair?", "Email", "Phone"],
            "content": db.execute("SELECT name, position, Committees.id AS committee_id, head_chair, email, phone_number FROM Committees JOIN Staffers ON Committees.id = Staffers.committee_id WHERE Staffers.name LIKE ?;", query),
            "empty": False
        }

        # Update the dictionary field to "empty" if the search returned no results
        if result["content"] == []:
            result["empty"] = True

        # Add this result to the total results list
        results.append(result)

    #debug print(results)

    # Render the page, sending the list of all results across all categories the user requested
    return render_template("results.html", results = results, search_in = search_in)