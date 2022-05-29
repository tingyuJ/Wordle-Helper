import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
# app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/search", methods=["POST"])
def search():

    letter1 = request.form.get("letter1").lower().strip()
    letter2 = request.form.get("letter2").lower().strip()
    letter3 = request.form.get("letter3").lower().strip()
    letter4 = request.form.get("letter4").lower().strip()
    letter5 = request.form.get("letter5").lower().strip()

    oletters = request.form.get("oletters").lower().strip()
    xletters = request.form.get("xletters").lower().strip()

    if not letter1 and not letter2 and not letter3 and not letter4 and not letter5 and not oletters and not xletters:
        flash('Require at least one input!')
        return redirect('/')

    for o in oletters:
        if o in xletters:
            flash("Letters can't be good and also wrong!")
            return redirect('/')

    answers = GetAnswers(letter1, letter2, letter3, letter4, letter5, oletters, xletters)

    if not answers:
        answers = ["No possible answers found. Check your inputs again!"]

    return render_template("index.html", answers=answers)




def GetAnswers(letter1, letter2, letter3, letter4, letter5, oletters, xletters):

    # 8250 words
    # Get all 5 letters words
    f = open("dictionary","r")

    dictionary = []

    for word in f.readlines():
        dictionary.append(word[0:5])

    f.close()

    # Get possible result
    result = []

    for word in dictionary:
        isOk = True

        # check letter1
        if letter1 and letter1 != word[0]:
            continue

        # check letter2
        if letter2 and letter2 != word[1]:
            continue

        # check letter3
        if letter3 and letter3 != word[2]:
            continue

        # check letter4
        if letter4 and letter4 != word[3]:
            continue

        # check letter5
        if letter5 and letter5 != word[4]:
            continue

        # check oletters
        for o in oletters:
            if o not in word:
                isOk = False
                break

        if not isOk:
            continue

        # check xletters
        for x in xletters:
            if x in word:
                isOk = False
                break

        if not isOk:
            continue

        result.append(word)

    return result

if __name__=="__main__":
    app.run()




