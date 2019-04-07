from flask import Flask, redirect, request, session, url_for, render_template, jsonify
from flask_session import Session
import requests
from tempfile import mkdtemp
import sqlite3


# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = sqlite3.connect("data//database.db")

@app.route("/")
def index():
	""" Show logged in user the welcome page """

	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("email"):
            return redirect("/asd")

        # ensure password was submitted
        elif not request.form.get("pwd"):
            return redirect("/addddddd")

        # query database for username
        query = "SELECT * FROM user_info WHERE email =  '{email}'".format(email = request.form.get("email"))
        rows = db.execute(query)
        rows = rows.fetchall()

        # ensure username exists and password is correct
        if len(rows) != 1 or not request.form.get("pwd") == rows[0][3]:
            return redirect("/e56e")

        # remember which user has logged in
        session["user_id"] = rows[0][0]
        session['uname'] = rows[0][1]

    # redirect user to home page
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if form is submitted via post
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return redirect(url_for("register"))

        # ensure password was submitted
        elif not request.form.get("password"):
            return redirect(url_for("register"))

        # ensure they retype the password again
        elif not request.form.get("re_password"):
            return redirect(url_for("register"))

        # ensure that the email is unique
        query = "SELECT * from user_info where email = '{email}'".format(email = request.form.get('email'))
        rows = db.execute(query)
        rows = rows.fetchone()
        if rows:
            return redirect(url_for("register"))
		

        # enusre both password fields have same values
        if request.form.get("password") != request.form.get("re_password"):
            return redirect(url_for("register"))

        # register the user into the database
        try:
            pwd = request.form.get("password")
            query = "INSERT into user_info(username,email,  pwd) VALUES('{uname}', '{email}', '{pwd}')".format(uname = request.form.get("username") , email =  request.form.get("email") , pwd =  pwd)
            db.execute(query)
            db.commit()
        except:
            print("105 error")
            return redirect("/")

        # log in the registered user
        query = "SELECT * FROM user_info WHERE email = '{email}'".format(email = request.form.get("email"))
        rows = db.execute(query).fetchall()
        session["user_id"] = rows[0][0]
        session["uname"] = rows[0][1]

        # redirect user to home page
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

"""
Gives back the 20 recommended song for the user in json
"""
@app.route("/getSonglist", methods = ["GET"])
def getSonglist():
	# get the userid and check the interation
	user = request.form.get("uid")

	query = "Select * FROM user_data WHERE u_id = '{user}';".format(user = user)
	rows = db.execute(query).fetchall()

	songs_interacted = len(rows)


	songs_list = []
	reader = ''

	# TODO : if user is new show songs based on popularity
	if songs_interacted < 2:
		with open("data//popular_songs.txt", "r") as file:
			i = 0
			for line in file:
				songs_list.append(line.strip())
				i += 1
				if i >= 20:
					break
		reader = [{"s_id": item, "title": item} for item in songs_list if item]

	# TODO : If user have given feedback for less then 20 songs show songs by collaborative filtering

	# TODO : else show similiar songs on basis of the feedback

	return jsonify(reader)

"""
Gets the feedback of user for a song
and save it to db
"""
@app.route("/getFeedback", methods=["GET"])
def saveFeedback():
	u_id = request.form.get("uid")
	song_id = request.form.get("s_id")
	feedback = request.form.get("feedback")

	query = "INSERT INTO user_data(u_id, song_id, feedback, play_count) VALUES('{uid}', '{song}', '{feedb}', '1')".format(uid=u_id, song=song_id, feedb=feedback)
	db.execute(query)
	db.commit()

	return jsonify("success")

