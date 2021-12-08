import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
idVal = 0

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///roomies.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def home():
    # Forget any user_id
    session.clear()

    return render_template("login.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Quiz"""
    if request.method == "POST":
        # Gather input from the form
        name = request.form.get("name")
        gender = request.form.get("gender")
        year = request.form.get("year")
        personality = request.form.get("personality")
        sleep = request.form.get("sleep")

        print("id")
        print(session["user_id"])

        # Insert values into SQL database for user
        db.execute("UPDATE users SET Name = ?, Gender = ?, Year = ?, Personality = ?, Sleep = ?, takenForm = 1 WHERE username = ?", name, gender, year, personality, sleep, session["user_id"])
        rows = db.execute("SELECT * FROM users WHERE username = ?", session["user_id"])
        print("after quiz sql")
        print(rows[0])

        return render_template("index.html")
    else:
        return render_template("quiz.html")

@app.route("/match")
@login_required
def match():
    # Get number of users
    numOfUsers = db.execute("SELECT COUNT(username) FROM users")[0]['COUNT(username)']
    # Get values from SQL database for current user
    currentUser = db.execute("SELECT * FROM users WHERE username = ?", session["user_id"])
    userBool = currentUser[0]["takenForm"]
    maxMatches = 0
    matchedUser = ""
    print(currentUser)

    # Ensure that user has filled out the quiz
    if userBool == 0:
        return apology("Please fill out quiz first", 400)
    else:
        # Iterate through all rows and keep track of person with most matches
        for i in range(numOfUsers):
            selectedUser = db.execute("SELECT * FROM users WHERE ID = ?", i)
            sameAnswers = 0
            print("current user")
            print(currentUser)
            if selectedUser[0]["ID"] != currentUser[0]["ID"]:
                print("selected user")
                print(selectedUser)
                # Gender
                if selectedUser[0]["Gender"] == currentUser[0]["Gender"]:
                    sameAnswers += 1
                # Year
                if selectedUser[0]["Year"] == currentUser[0]["Year"]:
                    sameAnswers += 1
                # Personality
                if selectedUser[0]["Personality"] == currentUser[0]["Personality"]:
                    sameAnswers += 1
                # Sleep
                if selectedUser[0]["Sleep"] == currentUser[0]["Sleep"]:
                    sameAnswers += 1
            if sameAnswers > maxMatches:
                maxMatches = sameAnswers
                matchedUser = selectedUser[0]["Name"]
            print(matchedUser)
        return render_template("match.html", matchName = matchedUser, matchGender = selectedUser[0]["Gender"], matchYear = selectedUser[0]["Year"], 
        matchPers = selectedUser[0]["Personality"], matchSleep = selectedUser[0]["Sleep"])

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["username"]

        print("sql call")
        print(rows[0])

        # Redirect user to home page
        return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    global idVal
    """Register user"""
    if request.method == "POST":
        print(idVal)
        if not request.form.get("username"):
            return apology("Must provide username", 400)
        if not request.form.get("password"):
            return apology("Must provide password", 400)
        if not request.form.get("confirmation"):
            return apology("Passwords must match", 400)

        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if db.execute("SELECT id FROM users WHERE username = ?", name):
            return apology("Username taken", 400)
        
        if password == confirmation:
            password_hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash, takenForm, ID) VALUES(?, ?, 0, ?)", name, password_hash, idVal)
            session["user_id"] = name
            idVal += 1
            print(idVal)

            return render_template("index.html")

        else:
            return apology("Passwords must match", 400)
    

    else:
        return render_template("register.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
