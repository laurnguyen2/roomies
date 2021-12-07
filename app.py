import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

def create_portfolio():
    rows = db.execute("SELECT symbol, SUM(shares) AS shares_owned FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
    
    portfolio = {}
    stocks = []
    total = 0
    
    for row in rows:
        stock = lookup(row["symbol"])
        stock["shares"] = row["shares_owned"]
        stock["value"] = stock["shares"] * stock["price"]
        total += stock["value"]
        stocks.append(stock)
    
    portfolio["stocks"] = stocks
    portfolio["total"] = total
    
    return portfolio

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def quiz():
    """Quiz"""
    if request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")
        year = request.form.get("year")
        personality = request.form.get("personality")
        sleep = request.form.get("sleep")

        db.execute("INSERT INTO profiles VALUES (?, ?, ?, ?, ?)", name, gender, year, personality, sleep)
        return render_template("buy.html")
    else:
        return render_template("quiz.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Please input a symbol", 400)
        
        stock = lookup(request.form.get("symbol"))
        if stock is None:
            return apology("Stock not found", 400)
        
        if not request.form.get("shares") or not request.form.get("shares").isnumeric():
            return apology("Please provide number of shares to purchase", 400)
        shares = float(request.form.get("shares"))
        if int(shares) != shares or int(shares) <= 0:
            return apology("Shares must be a positive integer", 400)

        sum = stock["price"] * int(shares)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
       
        if cash >= sum:
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transaction_value) VALUES (?, ?, ?, ?, ?)", session["user_id"], stock["symbol"], shares, stock["price"], sum)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - sum, session["user_id"])

            return redirect("/")

        else:
            return apology("Insufficient funds", 400)

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, price, shares, transaction_time FROM transactions WHERE user_id = ?", session["user_id"])

    for row in rows:
        if row["shares"] < 0:
            row["type"] = "sell"
        else:
            row["type"] = "buy"

    return render_template("history.html", transactions=rows)


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
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Please input a symbol", 400)
        
        stock = lookup(request.form.get("symbol"))
        if stock is None:
            return apology("Stock not found", 400)

        return render_template("quoted.html", symbol=stock["symbol"], stock_name=stock["name"], current_price=usd(stock["price"]))
    
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        
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
            user = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, password_hash)

            session["user_id"] = user

            return redirect("/")

        else:
            return apology("Passwords must match", 400)
    

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Please input a symbol", 400)
        stock = lookup(request.form.get("symbol"))
        if stock is None:
            return apology("Stock not found", 400)
        
        if not request.form.get("shares"):
            return apology("Please provide number of shares", 400)
        shares = float(request.form.get("shares"))
        if int(shares) != shares or int(shares) <= 0:
            return apology("Shares must be a positive integer", 400)

        owned = db.execute("SELECT SUM(shares) FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], stock["symbol"])
        if len(owned) != 1:
            return apology("You do not own this stock", 400)
        num_owned = owned[0]["SUM(shares)"]
        if num_owned < int(shares):
            return apology("You do not have enough shares", 400)

        sum = stock["price"] * int(shares)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
       
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transaction_value) VALUES (?, ?, ?, ?, ?)", session["user_id"], stock["symbol"], -shares, stock["price"], -sum)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + sum, session["user_id"])
        
        return redirect("/")

    else:
        symbols = []
        stocks = create_portfolio()["stocks"]
        for stock in stocks:
            symbols.append(stock["symbol"])
        return render_template("sell.html", symbols=symbols)

@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    if request.method == "POST":
        
        if not request.form.get("cash") or not request.form.get("cash").isnumeric():
            return apology("Please input a valid amount", 400)
        add_cash = float(request.form.get("cash"))
        if add_cash <= 0:
            return apology("Amount must be positive", 400)

        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", add_cash + current_cash, session["user_id"])

        return redirect("/")

    else:
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        return render_template("cash.html", cash=current_cash)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
