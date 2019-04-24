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

# connecting to the Database
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


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return render_template("logout.html")


"""
Gives back the 20 recommended song for the user in json
"""
@app.route("/getSonglist", methods = ["GET"])
def getSonglist():
	# get the userid and check the interation
	user = request.args.get("uid")

	query = "Select * FROM user_data WHERE u_id = '{user}';".format(user = user)
	rows = db.execute(query).fetchall()

    # number of songs user had interacted
	songs_interacted = len(rows)

	songs_list = []
	songs_liked = set()
	songs_disliked = set()

    # storing the song_id of song user liked and disliked
	for row in rows:
		if row[2] == 2:
			songs_disliked.add(row[1])
		else:
			songs_liked.add(row[1])

	reader = ''

	#  if user is new show songs based on popularity
	if songs_interacted < 9:
		query = "SELECT * FROM tracks_details WHERE t_id < 50"
		rows = db.execute(query).fetchall()

		for row in rows:
			if not row[1] in songs_disliked:
				songs_list.append([ row[1], row[2], row[3]])
		reader = [{"s_id": item[0], "artist" : item[1], "title": item[2]} for item in songs_list if item]

	else:
        # else show similiar songs on basis of the feedback of songs rated by user
		import KNN
		songs = KNN.getRecommendedSongs(songs_liked)
		reader = [{"s_id": item[0], "artist" : item[2], "title": item[1]} for item in songs if item and item[0] not in songs_disliked]

	return jsonify(reader)


"""
Gets the feedback of user for a song
and save it to db
"""
@app.route("/getFeedback", methods=["GET"])
def saveFeedback():
	u_id = request.args.get("uid")
	song_id = request.args.get("s_id")
	feedback = request.args.get("feedback")

	# check wether user had previously rated the song or not
	query = "SELECT feedback, play_count FROM user_data WHERE u_id = {uid} AND song_id = '{sid}'".format(uid = u_id, sid = song_id)
	row = db.execute(query).fetchone()
	if row:
		# if old feedback matches new one
		if row[0] == feedback:
			# update the play count
			query = "UPDATE user_data SET play_count = play_count + 1 WHERE u_id = {uid} AND song_id = '{sid}'".format(uid = u_id, sid = song_id)
			db.execute(query)
		else:
			query = "UPDATE user_data SET feedback = {fb} WHERE u_id = {uid} AND song_id = '{sid}'".format(fb = feedback, uid = u_id, sid = song_id)
			db.execute(query)
	else:
		# its a new song of user save it
		query = "INSERT INTO user_data(u_id, song_id, feedback, play_count) VALUES('{uid}', '{song}', '{feedb}', '1')".format(uid=u_id, song=song_id, feedb=feedback)
		db.execute(query)
		db.commit()

	return jsonify("Saved")


@app.route("/getUserSongs", methods=["GET"])
def getUserSongs():
	"""
	Returns list of songs user liked
	"""
	u_id = session["user_id"]
	query = "SELECT DISTINCT track_id, artist, title FROM tracks_details WHERE track_id IN (SELECT song_id FROM user_data WHERE u_id = '{uid}' AND feedback=3)".format(uid = u_id)
	rows = db.execute(query).fetchall()

	songs = [{"s_id": item[0], "artist" : item[1], "title": item[2]} for item in rows if item]
	print(songs)
	return render_template("songs.html", songs = songs)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == 'POST':
        # query database for username
        rows = db.execute("SELECT * FROM user_info WHERE u_id = {uid}".format([session["user_id"]])).fetchone()

        # ensure password is correct
        if len(rows) != 1 or not request.form.get("oldpass") ==  rows[3]:
            
            return redirect(url_for("settings"))

        # ensure the new password aren't blank
        if request.form.get("newpass") is '' or request.form.get("newpassr") is '':
            
            return redirect(url_for("settings"))

        # ensure the new password are same
        if (request.form.get("newpass")) != request.form.get("newpassr"):
            
            return redirect(url_for("settings"))

        # updating the password field
        
        db.execute("UPDATE user_info SET pwd = {newp}".format(newp = request.form.get("newpass"))).commit()

        return redirect(url_for("index"))
    else:
        return render_template("settings.html")