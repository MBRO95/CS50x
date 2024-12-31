import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":
        # Get users balance
        try:
            cashBalance = float(db.execute("SELECT cash FROM users WHERE id = ?",
                                session["user_id"])[0]['cash'])
        except:
            return apology("error retrieving balance info", 400)
        # Get users stocks value
        try:
            userTransactions = db.execute(
                "SELECT * FROM transactions WHERE user = ? ORDER BY datestamp", session["user_id"])
            stocks = {}
            # Check historical transactions
            for transaction in userTransactions:
                if transaction['symbol'] in stocks:
                    # Update existing stock record
                    stocks[transaction['symbol']]['shares'] += transaction['shares']
                    stocks[transaction['symbol']]['costBasis'] += transaction['order_amount']
                else:
                    # Create new stock record
                    stocks[transaction['symbol']] = dict(
                        shares=transaction['shares'], costBasis=transaction['order_amount'])
            # Determine current portfolio stock values
            portfolioBalance = 0
            stocksBalance = 0
            plTotal = 0
            for stock in stocks:
                try:
                    quote = lookup(stock)
                    if quote == None:
                        return apology("invalid symbol specified", 400)
                except:
                    return apology("error retrieving quote info", 400)
                stocks[stock]["currentPrice"] = quote["price"]
                stocks[stock]["positionValue"] = float(
                    quote["price"]) * float(stocks[stock]["shares"])
                # Sum portfolio balance
                portfolioBalance += stocks[stock]["positionValue"]
                stocksBalance += stocks[stock]["positionValue"]
                # Calculate Profit or Loss
                plTotal += (stocks[stock]["positionValue"] - stocks[stock]["costBasis"])
                if stocks[stock]["positionValue"] > stocks[stock]["costBasis"]:
                    stocks[stock]["pl"] = "+" + \
                        usd(stocks[stock]["positionValue"] - stocks[stock]["costBasis"])
                elif stocks[stock]["positionValue"] < stocks[stock]["costBasis"]:
                    stocks[stock]["pl"] = "-" + \
                        usd(stocks[stock]["costBasis"] - stocks[stock]["positionValue"])
                stocks[stock]["positionValue"] = usd(stocks[stock]["positionValue"])
            portfolioBalance = usd(portfolioBalance + cashBalance)
            cashBalance = usd(cashBalance)
            stocksBalance = usd(stocksBalance)
            plTotal = usd(plTotal)
        except:
            return apology("error retrieving transaction info", 400)
        return render_template("index.html", stocks=stocks, cashBalance=cashBalance, portfolioBalance=portfolioBalance, stocksBalance=stocksBalance, plTotal=plTotal)
    else:
        return apology("GETs only", 403)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide requested share count", 400)
        # Ensure shares is valid
        if not request.form.get("shares").isnumeric():
            return apology("must provide numeric share count", 400)
        try:
            balance = float(db.execute("SELECT cash FROM users WHERE id = ?",
                            session["user_id"])[0]['cash'])
        except:
            return apology("error retrieving balance info", 400)
        try:
            quote = lookup(request.form.get("symbol"))
            if quote == None:
                return apology("invalid symbol specified", 400)
        except:
            return apology("error retrieving quote info", 400)

        # Calculate order size and determine fulfillment status
        orderSize = quote["price"] * float(request.form.get("shares"))
        fulfillable = False
        if orderSize <= balance:
            fulfillable = True

        if fulfillable == True:
            try:
                newBalance = balance - orderSize
                confirmation = db.execute(
                    "UPDATE users SET cash = ? WHERE id = ?", newBalance, session["user_id"])
            except:
                return apology("error executing transaction", 400)
            try:
                # https://www.postgresql.org/docs/current/sql-createtable.html
                # https://www.postgresql.org/docs/current/sql-createindex.html
                db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user NUMERIC NOT NULL, type TEXT NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, share_price NUMERIC NOT NULL, order_amount NUMERIC NOT NULL, datestamp DATETIME NOT NULL DEFAULT (GETDATE()))")
                db.execute("CREATE UNIQUE INDEX IF NOT EXISTS id ON transactions (id)")
                db.execute("CREATE INDEX IF NOT EXISTS user ON transactions (user)")
                db.execute("CREATE INDEX IF NOT EXISTS symbol ON transactions (symbol)")
                db.execute("CREATE INDEX IF NOT EXISTS type ON transactions (type)")
                db.execute("INSERT INTO transactions (user, type, symbol, share_price, shares, order_amount, datestamp) VALUES (?, ?, ?, ?, ?, ?, ?)", int(
                    session["user_id"]), "BUY", quote["symbol"], quote["price"], int(request.form.get("shares")), orderSize, datetime.now())

                # Redirect user to home page
                return redirect("/")
            except:
                return apology("error creating transaction ledger", 400)
        else:
            return apology("insufficient funds", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of transactions"""
    # User reached route via GET (as by loading a webpage)
    if request.method == "GET":
        try:
            userTransactions = db.execute(
                "SELECT * FROM transactions WHERE user = ? ORDER BY datestamp", int(session["user_id"]))
        except:
            return apology("transaction lookup error", 400)
        stockValuesNow = {}
        for transaction in userTransactions:
            try:
                quote = lookup(transaction['symbol'])
                if quote == None:
                    return apology("invalid symbol specified", 400)
            except:
                return apology("error retrieving quote info", 400)
            # Create new stock price record
            stockValuesNow[transaction['symbol']] = dict(price=quote["price"])
            # https://stackoverflow.com/questions/4828406/import-a-python-module-into-a-jinja-template
        return render_template("history.html", transactions=userTransactions, stockValuesNow=stockValuesNow, usd=usd)
    else:
        return apology("Only GET supported", 403)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        try:
            quote = lookup(request.form.get("symbol"))
            if quote == None:
                return apology("invalid symbol specified", 400)
            quote["price"] = usd(quote["price"])
        except:
            return apology("error retrieving info", 400)
        return render_template("quoted.html", quote=quote)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation do not match", 400)

        # Attempted registration into database
        try:
            result = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))
        except:
            return apology("Registration Error", 400)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares", 400)

        # Ensure shares is valid
        if not request.form.get("shares").isnumeric():
            return apology("must provide positive numeric share count", 400)

        # Ensure shares is fulfillable
        sharesHeld = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = ? AND user = ?", request.form.get(
            "symbol"), session["user_id"])
        if not int(request.form.get("shares")) < int(sharesHeld[0]["SUM(shares)"]):
            return apology("insufficient shares", 400)

        # Execute sale
        try:
            # Lookup stock
            try:
                balance = float(db.execute("SELECT cash FROM users WHERE id = ?",
                                session["user_id"])[0]['cash'])
            except:
                return apology("error retrieving balance info", 400)
            try:
                quote = lookup(request.form.get("symbol"))
                if quote == None:
                    return apology("invalid symbol specified", 400)
            except:
                return apology("error retrieving quote info", 400)

            # Calculate order size
            orderSize = quote["price"] * float(request.form.get("shares"))

            # Execute sell transaction
            db.execute("INSERT INTO transactions (user, type, symbol, share_price, shares, order_amount, datestamp) VALUES (?, ?, ?, ?, ?, ?, ?)", int(
                session["user_id"]), "SELL", quote["symbol"], quote["price"], -abs(int(request.form.get("shares"))), -abs(orderSize), datetime.now())

            # Credit cash balance
            try:
                newBalance = balance + orderSize
                confirmation = db.execute(
                    "UPDATE users SET cash = ? WHERE id = ?", newBalance, session["user_id"])
            except:
                return apology("error crediting cash balance", 400)

            # Redirect user to home page
            return redirect("/")
        except:
            return apology("error executing sale", 400)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        userStocks = db.execute(
            "SELECT DISTINCT symbol FROM transactions WHERE user = ?", session["user_id"])
        return render_template("sell.html", userStocks=userStocks)
