import json
import os
from functools import wraps

import requests
from cs50 import SQL
from flask import Flask, render_template, request, redirect, url_for, session
from oauthlib.oauth2 import WebApplicationClient

# Configure application
app = Flask(__name__)
app.secret_key = b'super secret key'
app.SESSION_COOKIE_DOMAIN = 'ymun.org'
app.SERVER_NAME = 'ymun.org'

if __name__ == "__main__":
    app.run(ssl_context="adhoc")

# Configure Google Oauth stuff
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            print("you are not logged in")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    # response.headers["Pragma"] = "no-cache"
    return response


# Old database
# db = SQL("sqlite:///data_XLVI.db")

# New Heroku Database
db = SQL(
    "postgres://hnqodbzrirphml:8c61d75015387e2141ba3db8d6072b730a4cc194646e09239f79226fc02f879a@ec2-174-129-255-37.compute-1.amazonaws.com:5432/ddlp8u4p34upr4")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    print("got response from google")

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    print(userinfo_response.json()["email"])
    session.clear()
    if "@ymun.org" in userinfo_response.json()["email"]:
        print("this worked")
        session["user_id"] = userinfo_response.json()["email"]
        session["user_picture"] = userinfo_response.json()["picture"]
        session["user_name"] = userinfo_response.json()["given_name"]
    else:
        return "You are not authorized to access this application.", 400

    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Display the list of all committees
@app.route("/committees", methods=["GET"])
@login_required
def displayCommittees():
    if request.method == "GET":
        print(session["user_id"])
        print(session["user_picture"])
        print(session["user_name"])
        # Select information about all the committees, as well as the head chair for each committee
        committees = db.execute(
            "SELECT Committees.*, Staffers.name FROM Committees JOIN Staffers ON Committees.id = Staffers.committee_id WHERE Staffers.head_chair = '1';")

        # debug print(committees)

        # Render the page
        return render_template('committees.html', committees=committees)


# Individual Committee Information Page
@app.route("/display-committee", methods=["GET", "POST"])
@login_required
def displayCommitteeInfo():
    # The user has requested to see information about a specific committee
    if request.method == "GET":
        # get committee ID from GET request parameter
        committee_id = request.args.get('committee_id')

        # debug print(committee_id)

        # Select info about the requested committee
        committee = db.execute("SELECT * FROM Committees WHERE id = ?;", committee_id)[0]

        # Select info about staffers
        staffers = db.execute("SELECT * FROM Staffers WHERE committee_id = ?;", committee_id)

        # Select the list of delegates in the requested committee, using the "assignedname" used in position sheets that were sent to advisors
        delegates = db.execute("SELECT * FROM Delegates WHERE committee_assigned = ?", committee["assignedname"])

        # debug print(committee)

        # Render the page
        return render_template('display-committee.html', delegates=delegates, committee_id=committee_id,
                               committee=committee, staffers=staffers)


# Display the list of all delegations
@app.route("/delegations", methods=["GET"])
@login_required
def displayDelegations():
    if request.method == "GET":
        # Select information about all the delegations, as well as the point of contact advisor for each delegation
        delegations = db.execute(
            "SELECT * FROM Delegations JOIN Advisors ON Delegations.school_name = Advisors.school WHERE Advisors.point_of_contact = '1' ORDER BY school_name;")

        # debug print(delegations)

        # Render the page
        return render_template('delegations.html', delegations=delegations)


# Individual Delegation Information Page
@app.route("/display-delegation", methods=["GET", "POST"])
@login_required
def displayDelegationInfo():
    # The user has requested to see information about a specific delegation
    if request.method == "GET":
        # get delegation school name from GET request parameter
        school_name = request.args.get('school_name')

        # Select info about the requested delegation, as well as the point of contact advisor for the delegation
        delegation = db.execute(
            "SELECT * FROM Delegations JOIN Advisors ON Delegations.school_name = Advisors.school WHERE Advisors.point_of_contact = '1' AND school_name = ?;",
            school_name)[0]

        # Select info about advisors
        advisors = db.execute("SELECT * FROM Advisors WHERE school = ?;", school_name)

        # Select the list of delegates in the requested delegation, as well as the full name and internal abbreviation of the committee that they are in
        delegates = db.execute(
            "SELECT Delegates.*, Committees.id as committee_id, Committees.fullname as committee_name FROM Delegates JOIN Committees ON Delegates.committee_assigned = committees.assignedname WHERE school = ?",
            school_name)

        print(delegates)

        # Render the page
        return render_template('display-delegation.html', delegates=delegates, school_name=school_name,
                               delegation=delegation, advisors=advisors)


Display the list of rooms
@app.route("/rooming", methods=["GET"])
def displayRooms():
    if request.method == "GET":
        # Select information about all the committees, as well as the head chair for each committee
        committees = db.execute(
            "SELECT organ, fullname, day1, day2, day3, day4 FROM Committees;")

        # debug print(committees)

        # Render the page
        return render_template('committees.html', committees=committees)

@app.route("/attendance", methods=["GET"])
def displayAbsences():
    if request.method == "GET":
        return render_template('absences.html')


@app.route("/s1", methods=["GET"])
def s1():
    if request.method =="GET":
        absences = db.execute("SELECT Attendance.name AS delegate_name, Attendance.school, Delegates.committee_assigned, Delegates.position_name, Advisors.name AS advisor_name, Advisors.us_phone_number FROM Attendance JOIN Advisors ON Attendance.school = Advisors.school JOIN Delegates ON Attendance.name = Delegates.name AND Attendance.school = Delegates.school WHERE Advisors.point_of_contact = '1' AND (s1 ='0' OR s1 = '') ORDER BY Attendance.school;")

        #debug print(absences)

        return render_template('s1.html', absences = absences)

@app.route("/s2", methods=["GET"])
def s2():
    if request.method =="GET":
        absences = db.execute("SELECT Attendance.name AS delegate_name, Attendance.school, Delegates.committee_assigned, Delegates.position_name, Advisors.name AS advisor_name, Advisors.us_phone_number FROM Attendance JOIN Advisors ON Attendance.school = Advisors.school JOIN Delegates ON Attendance.name = Delegates.name AND Attendance.school = Delegates.school WHERE Advisors.point_of_contact = '1' AND (s2 ='0' OR s2 = '') ORDER BY Attendance.school;")

        #debug print(absences)

        return render_template('s2.html', absences = absences)

@app.route("/s3", methods=["GET"])
def s3():
    if request.method =="GET":
        absences = db.execute("SELECT Attendance.name AS delegate_name, Attendance.school, Delegates.committee_assigned, Delegates.position_name, Advisors.name AS advisor_name, Advisors.us_phone_number FROM Attendance JOIN Advisors ON Attendance.school = Advisors.school JOIN Delegates ON Attendance.name = Delegates.name AND Attendance.school = Delegates.school WHERE Advisors.point_of_contact = '1' AND (s3 ='0' OR s3 = '') AND s2 != '0' AND s2 != '' ORDER BY Attendance.school;")

        #debug print(absences)

        return render_template('s3.html', absences = absences)

@app.route("/s4", methods=["GET"])
def s4():
    if request.method =="GET":
        absences = db.execute("SELECT Attendance.name AS delegate_name, Attendance.school, Delegates.committee_assigned, Delegates.position_name, Advisors.name AS advisor_name, Advisors.us_phone_number FROM Attendance JOIN Advisors ON Attendance.school = Advisors.school JOIN Delegates ON Attendance.name = Delegates.name AND Attendance.school = Delegates.school WHERE Advisors.point_of_contact = '1' AND (s4 ='0' OR s4 = '') ORDER BY Attendance.school;")

        #debug print(absences)

        return render_template('s4.html', absences = absences)

@app.route("/s5", methods=["GET"])
def s5():
    if request.method =="GET":
        absences = db.execute("SELECT Attendance.name AS delegate_name, Attendance.school, Delegates.committee_assigned, Delegates.position_name, Advisors.name AS advisor_name, Advisors.us_phone_number FROM Attendance JOIN Advisors ON Attendance.school = Advisors.school JOIN Delegates ON Attendance.name = Delegates.name AND Attendance.school = Delegates.school WHERE Advisors.point_of_contact = '1' AND (s5 ='0' OR s5 = '') AND s4 != '0' AND s4 != '' ORDER BY Attendance.school;")

        #debug print(absences)

        return render_template('s5.html', absences = absences)

@app.route("/s6", methods=["GET"])
def s6():
    if request.method =="GET":
        absences = db.execute("SELECT Attendance.name AS delegate_name, Attendance.school, Delegates.committee_assigned, Delegates.position_name, Advisors.name AS advisor_name, Advisors.us_phone_number FROM Attendance JOIN Advisors ON Attendance.school = Advisors.school JOIN Delegates ON Attendance.name = Delegates.name AND Attendance.school = Delegates.school WHERE Advisors.point_of_contact = '1' AND (s6 ='0' OR s6 = '') AND s5 != '0' AND s5 != '' ORDER BY Attendance.school;")

        #debug print(absences)

        return render_template('s6.html', absences = absences)

@app.route("/s7", methods=["GET"])
def s7():
    if request.method =="GET":
        absences = db.execute("SELECT Attendance.name AS delegate_name, Attendance.school, Delegates.committee_assigned, Delegates.position_name, Advisors.name AS advisor_name, Advisors.us_phone_number FROM Attendance JOIN Advisors ON Attendance.school = Advisors.school JOIN Delegates ON Attendance.name = Delegates.name AND Attendance.school = Delegates.school WHERE Advisors.point_of_contact = '1' AND (s7 ='0' OR s7 = '') ORDER BY Attendance.school;")

        #debug print(absences)

        return render_template('s7.html', absences = absences)

# Display search results
@app.route("/results", methods=["GET"])
@login_required
def search():
    # Determine whether the user wants to search through all tables or a specific one
    search_in = request.args.get("search_in")

    # Get the query from the http request
    query = "%" + request.args.get("query").lower() + "%"

    # Initialize the results to an empty list
    results = []

    # Populate the results list with matches from the advisors table
    if search_in in ("advisors", "all"):

        # Format the matching advisors in a dictionary, adding information for the HTML template and headers
        result = {
            "type": "Advisors",
            "headers": ["Advisor Name", "School", "Phone", "Email"],
            "content": db.execute("SELECT name, school, us_phone_number, email FROM Advisors WHERE LOWER(name) LIKE ?;",
                                  query),
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
            "content": db.execute(
                "SELECT name, school, Committees.id AS committee_id, position_name FROM Delegates JOIN Committees ON Delegates.committee_assigned = Committees.assignedname WHERE LOWER(name) LIKE ?",
                query),
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
            "content": db.execute(
                "SELECT school_name AS school, country, delegate_count, advisor_count FROM Delegations WHERE LOWER(school_name) LIKE ?;",
                query),
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
            "content": db.execute(
                "SELECT Committees.id AS committee_id, fullname, size, name, phone_number, email FROM Committees JOIN Staffers ON Committees.id = Staffers.committee_id WHERE Staffers.head_chair = '1' AND LOWER(Committees.fullname) LIKE ?;",
                query),
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
            "content": db.execute(
                "SELECT name, position, Committees.id AS committee_id, head_chair, email, phone_number FROM Committees JOIN Staffers ON Committees.id = Staffers.committee_id WHERE LOWER(Staffers.name) LIKE ?;",
                query),
            "empty": False
        }

        # Update the dictionary field to "empty" if the search returned no results
        if result["content"] == []:
            result["empty"] = True

        # Add this result to the total results list
        results.append(result)

    # debug print(results)

    # Render the page, sending the list of all results across all categories the user requested
    return render_template("results.html", results=results, search_in=search_in)