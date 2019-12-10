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

@app.route("/", methods=["GET"])
def index():

    return render_template('homepage.html')

@app.route("/committees", methods=["GET", "POST"])
def displayCommittees():
    if request.method =="GET":
        committees = db.execute("SELECT * FROM Committees;")
        print(committees)
        print(committees[0])
        return render_template('committees.html', committees=committees)

@app.route("/delegations", methods=["GET"])
def displayDelegations():
    if request.method =="GET":
        delegations = db.execute("SELECT * FROM Delegations;")
        return render_template('delegations.html', delegations=delegations)

@app.route("/rooming", method=["GET"])
def displayRooms():
    if request.method =="GET":
        rooms = db.execute("SELECT * FROM Rooming;")
        return render_template('rooming.html', rooming=rooming)

@app.route("/absences", method=["GET"])
def displayAbsences():
    if request.method =="GET":
        return render_template('absences.html')

@app.route("/s1", method=["GET"])
def displays1():
    if request.method =="GET":
        s1 = db.execute("SELECT * FROM Attendance WHERE ")
        return render_template('s1.html')