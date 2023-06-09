from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from db_connections import db, logindb
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Define a function to get the current user
def get_current_user():
    # code to get the current user
    return session["username"]

# Define the issues table
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS issues (id INT AUTO_INCREMENT PRIMARY KEY, team_number INT, issue VARCHAR(255), details TEXT)")
cursor.close()

# Create the login table if it doesn't exist
cursor = logindb.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS login(username VARCHAR(255) NOT NULL PRIMARY KEY, password VARCHAR(255) NOT NULL, event_id VARCHAR(255) NOT NULL)")
cursor.close()


# Define the routes
@app.route("/")
def index():
    if "username" in session:
        if session["username"] == "mentor":
            session["is_mentor"] = "is_mentor"
        else:
            session["is_mentor"] = "is_not_mentor"
        user = get_current_user()
        return render_template("index.html", user=user, loggedin=True, is_mentor=session["is_mentor"])
    else:
        return render_template("index.html", loggedin=False)


@app.route("/submit", methods=["POST"])
def submit():
    team_number = request.form["team_number"]
    issue = request.form["issue"]
    details = request.form["details"]

    # Insert the issue into the issues table
    cursor = db.cursor()
    cursor.execute("INSERT INTO issues (team_number, issue, details) VALUES (%s, %s, %s)",
                   (team_number, issue, details))
    db.commit()
    cursor.close()

    return redirect(thankyou)


@app.route("/thankyou")
def thankyou():
    return "Thank you for your submission. Your issue has been received and will be addressed shortly."


@app.route("/carer")
def carer():
    if session["username"] == "mentor":
        session["is_mentor"] = "is_mentor"
    else:
        session["is_mentor"] = "is_not_mentor"
    if "username" in session:
        user = get_current_user()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM issues")
        issues = cursor.fetchall()
        cursor.close()
        print(issues)  # Add this line to check the value of the issues variable
        print(session["is_mentor"])
        print(session["username"])
        return render_template("carer.html", issues=issues, user=user, loggedin=True, is_mentor=session["is_mentor"])
    else:
        return redirect("/login")


# Define login page route
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if "username" in session:
        return redirect("carer")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # event_id = request.form["event_id"]
        try:
            cursor = logindb.cursor()
            cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            if user:
                session["username"] = user[0]
                user = get_current_user()
                if session["username"] == "mentor":
                    session["is_mentor"] = "is_mentor"
                else:
                    session["is_mentor"] = "is_not_mentor"
                return redirect("/carer")
            else:
                error = "Invalid username, password, or eventID"
                return render_template("login.html", error=error)
        except mysql.connector.Error as error:
            print("Failed to read record from MySQL table: {}".format(error))
            error = "Failed to read record from database"
            return render_template("login.html", error=error, is_mentor=session["is_mentor"])
    else:
        return render_template("login.html")


# Define logout route
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


# Define create account route
@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if "username" in session:
        if session["username"] == "mentor":
            session["is_mentor"] = "is_mentor"
        else:
            session["is_mentor"] = "is_not_mentor"
        user = get_current_user()
        if "username" in session:
            if session["username"] == "mentor":
                if request.method == "POST":
                    username = request.form["username"]
                    password = request.form["password"]
                    event_ID = request.form["eventID"]
                    try:
                        cursor = logindb.cursor()
                        cursor.execute("INSERT INTO login (username, password, event_id) VALUES (%s, %s, %s)",
                                       (username, password, event_ID))
                        logindb.commit()
                        cursor.close()
                        return redirect("/carer")
                    except mysql.connector.Error as error:
                        print("Failed to insert record into MySQL table: {}".format(error))
                        return render_template("create_account.html", error="Failed to create account", user=user,
                                               loggedin=True, is_mentor=session["is_mentor"])
                else:
                    return render_template("create_account.html", user=user, loggedin=True,
                                           is_mentor=session["is_mentor"])
            else:
                return redirect("login")
        else:
            return redirect("login")
    else:
        return redirect("login")


# Define delete account route
@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if "username" in session:
        if session["username"] == "mentor":
            session["is_mentor"] = "is_mentor"
        else:
            session["is_mentor"] = "is_not_mentor"
        user = get_current_user()
        if "username" in session:
            if session["username"] == "mentor":
                if request.method == "POST":
                    username = request.form["username"]
                    try:
                        cursor = logindb.cursor()
                        cursor.execute("DELETE FROM login WHERE username = %s", (username,))
                        logindb.commit()
                        cursor.close()
                        return redirect("/carer")
                    except mysql.connector.Error as error:
                        print("Failed to delete record from MySQL table: {}".format(error))
                        return render_template("delete_account.html", error="Failed to delete account")
                else:
                    return render_template("delete_account.html", user=user, loggedin=True,
                                           is_mentor=session["is_mentor"])
            else:
                return redirect("login")
        else:
            return redirect("login")
    else:
        return redirect("login")


# Define mentors route
@app.route('/mentors')
def mentors():
    if "username" in session:
        if session["username"] == "mentor":
            session["is_mentor"] = "is_mentor"
        else:
            session["is_mentor"] = "is_not_mentor"
        user = get_current_user()
        if "username" in session:
            if session["username"] == "mentor":
                cursor = db.cursor()
                cursor.execute("SELECT * FROM login.login")
                accounts = cursor.fetchall()
                cursor.close()
                print(accounts)  # Add this line to check the value of the issues variable
                return render_template("mentors.html", accounts=accounts, user=user, loggedin=True,
                                       is_mentor=session["is_mentor"])
            else:
                return redirect("login")
        else:
            return redirect("login")
    else:
        return redirect("login")


#                 ----------------------------------------------------------
#                 ------------------  A P I  R O U T E S  ------------------
#                 ----------------------------------------------------------

@app.route("/api/issues")
def get_issues():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM issues")
    issues = cursor.fetchall()
    cursor.close()
    return jsonify(issues)


@app.route("/api/issues/<int:team_number>")
def get_issues_by_team(team_number):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM issues WHERE team_number = %s", (team_number,))
    issues = cursor.fetchall()
    cursor.close()
    return jsonify(issues)


@app.route("/api/issues/<issue>")
def get_issues_by_issue(issue):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM issues WHERE issue = %s", (issue,))
    issues = cursor.fetchall()
    cursor.close()
    return jsonify(issues)


@app.route("/api/issues/<int:team_number>/<issue>")
def get_issues_by_team_and_issue(team_number, issue):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM issues WHERE team_number = %s AND issue = %s", (team_number, issue))
    issues = cursor.fetchall()
    cursor.close()
    return jsonify(issues)


# Run the app
if __name__ == "__main__":
    app.run()
