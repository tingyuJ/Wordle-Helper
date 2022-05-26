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


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    userId = session["user_id"]

    results = db.execute("SELECT * FROM 'index' WHERE user_id = ?", userId)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", userId)
    cash = float(cash[0]["cash"])

    rows = []
    total = 0

    for r in results:

        current = lookup(r["symbol"])

        row = {
            "symbol": r["symbol"],
            "name": current["name"],
            "shares": int(r["shares"]),
            "price": float(current["price"]),
            "total": float(current["price"]) * int(r["shares"])
        }

        total += row["total"]

        rows.append(row)

    return render_template("index.html", rows=rows, cash=cash, total=total+cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        userId = session["user_id"]
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        result = lookup(symbol)

        if not result:
            return apology("Invalid symbol", 400)

        cash = db.execute("SELECT cash FROM users WHERE id = ?", userId)

        name = result["name"]
        symbol = result["symbol"]
        price = result["price"]

        if float(price) * int(shares) > float(cash[0]["cash"]):
            return apology("Failed. Cannot afford the number of shares at the current price.", 400)

        owned_shares = db.execute("SELECT shares FROM 'index' WHERE user_id = ? and symbol = ?", userId, symbol)

        if not owned_shares:
            db.execute("INSERT INTO 'index' (user_id, symbol, shares) VALUES(?, ?, ?)", userId, symbol, shares)
        else:
            db.execute("UPDATE 'index' SET shares = ? WHERE user_id = ? and symbol = ?",
                       int(owned_shares[0]["shares"])+int(shares), userId, symbol)

        newBalance = float(cash[0]["cash"]) - float(price) * int(shares)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newBalance, userId)
        db.execute("INSERT INTO history (user_id, symbol, shares, price, transacted) VALUES(?, ?, ?, ?, datetime('now'))",
                   userId, symbol, shares, float(price))

        # Redirect user to home page
        flash('Bought!')
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    userId = session["user_id"]

    results = db.execute("SELECT * FROM history WHERE user_id = ?", userId)

    return render_template("history.html", rows=results)


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

        symbol = request.form.get("symbol")

        result = lookup(symbol)

        if not result:
            return apology("Invalid symbol", 400)

        name = result["name"]
        symbol = result["symbol"]
        price = result["price"]

        msg = f"A share of {name}. ({symbol}) costs {usd(price)}."

        return render_template("quote.html", msg=msg)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password or not confirmation:
            return apology("must provide password & confirm", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Username aleady exists
        if len(rows) == 1:
            return apology("Username aleady exists", 400)

        # Check if passwords match
        if password != confirmation:
            return apology("Password confirmation does not match with password", 400)

        # INSERT the new user into users
        id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # Auto log in
        session["user_id"] = id

        # Redirect user to home page
        flash('Register!')
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    userId = session["user_id"]

    if request.method == "GET":

        symbols = db.execute("SELECT symbol FROM 'index' WHERE user_id = ?", userId)

        return render_template("sell.html", symbols=symbols)

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("must select a stock and/or shares amount", 400)

        hodings = db.execute("SELECT shares FROM 'index' WHERE user_id = ? and symbol = ?", userId, symbol)

        if int(hodings[0]["shares"]) < int(shares):
            return apology("does not own that many shares of the stock to sell", 400)

        # sell
        current = lookup(symbol)
        price = current["price"]

        # update index
        db.execute("UPDATE 'index' SET shares = ? WHERE user_id = ? and symbol = ?",
                   int(hodings[0]["shares"])-int(shares), userId, symbol)

        # update users
        cash = db.execute("SELECT cash FROM users WHERE id = ?", userId)

        newBalance = float(cash[0]["cash"]) + float(price) * int(shares)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newBalance, userId)

        # update history
        db.execute("INSERT INTO history (user_id, symbol, shares, price, transacted) VALUES(?, ?, ?, ?, datetime('now'))",
                   userId, symbol, -int(shares), float(price))

        # Redirect user to home page
        flash('Sold!')
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
