import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# from helpers import apology, login_required, lookup, usd

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
# app.jinja_env.filters["usd"] = usd


# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/search", methods=["POST"])
def login():

    letter1 = request.form.get("letter1").lower()
    letter2 = request.form.get("letter2").lower()
    letter3 = request.form.get("letter3").lower()
    letter4 = request.form.get("letter4").lower()
    letter5 = request.form.get("letter5").lower()

    oletters = request.form.get("oletters").lower()
    xletters = request.form.get("xletters").lower()


    answers = GetAnswers(letter1, letter2, letter3, letter4, letter5, oletters, xletters)

    return render_template("index.html", answers=answers)




def GetAnswers(letter1, letter2, letter3, letter4, letter5, oletters, xletters):

    #Get all 5 letters words
    f = open("dictionary","r")

    dictionary = []

    for word in f.readlines():
        dictionary.append(word[0:5])

    f.close()



    # if oletters is null, use all letters
    allletters = "qazwsxedcrfvtgbyhnujmikolp"
    if xletters:
        temp = ""
        for o in allletters:
            if o not in xletters:
                temp += o
        allletters = temp

    print("allletters: " + allletters)
    #Get all possiblities
    answers = []

    for i in allletters:
        for j in allletters:
            for k in allletters:
                for m in allletters:
                    for n in allletters:

                        if letter1:
                            i = letter1
                        if letter2:
                            j = letter2
                        if letter3:
                            k = letter3
                        if letter4:
                            m = letter4
                        if letter5:
                            n = letter5

                        word = i + j + k + m + n

                        answers.append(word)
        # Clear dupicates to make room in memory for more combimations.
        # Otherwise the program will be killed b4 it run through all possibilities
        answers = list(dict.fromkeys(answers))

    # Remove the dupicates
    answers = list(dict.fromkeys(answers))
    # print(answers)

    # Rule out some answers with the x letters
    excluded = []

    if xletters:

        for x in xletters:
            # first time when excluded is empty. Check the ones that do not contain the x letter
            if not excluded:
                for ans in answers:
                    # print(ans)
                    # print(x)

                    if x not in ans:
                        # print("o")
                        excluded.append(ans)

            # remove the ones that has the other x letters
            else:
                tempList = []
                for ex in excluded:
                    # print(ex)

                    if x in ex:
                        # print("x")
                        tempList.append(ex)

                for i in tempList:
                    excluded.remove(i)

    else:
        excluded = answers


    # Get the ones that exist
    result = []

    for ans in excluded:
        if ans in dictionary:
            result.append(ans)


    goodResult = []
    if oletters:
        for o in oletters:
            for r in result:
                if o in r:
                    goodResult.append(r)
    goodResult = list(dict.fromkeys(goodResult))

    if goodResult:
        result = goodResult

    return result




