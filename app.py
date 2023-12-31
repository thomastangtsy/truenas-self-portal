import os
from config import config
from datetime import timedelta
from flask import Flask, flash, redirect, render_template, request, session, url_for
from truenas import TrueNAS

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)
app.config["TRUENAS"] = TrueNAS(config["endpoint"], config["api_key"], config["ignore_invalid_certificate"] != "1")

@app.route("/")
def index():
    if not has_logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    errors=[]
    if has_logged_in():
        return redirect(url_for("index"))

    if request.method == "POST" and "username" in request.form and "password" in request.form:
        validate = app.config["TRUENAS"].validate_password(request.form["username"], request.form["password"])
        if validate:
            session.clear()
            user_info = app.config["TRUENAS"].get_user_info(request.form["username"])
            session["user_id"] = str(user_info[0]["id"])
            session["username"] = str(user_info[0]["username"])
            return redirect(url_for("login"))
        
        errors.append("Incorrect username or password.")
    return render_template("login.html", errors=errors)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

@app.route("/update_password", methods=["GET", "POST"])
def update_password():
    errors=[]
    if not has_logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    if request.method == "POST" and "current_pw" in request.form and "new_pw" in request.form and "new_pw_retype" in request.form:
        validate = app.config["TRUENAS"].validate_password(session.get("username"), request.form["current_pw"])
        match_password = request.form["new_pw"] == request.form["new_pw_retype"]
        if validate and match_password:
            if app.config["TRUENAS"].update_password(session.get("user_id"), request.form["new_pw"]):
                session.clear()
                flash("Password updated."),
                flash("You are forced logout.")
                return redirect(url_for("login"))
            errors.append("Failed to update password.")
        else:
            errors.append("Current password incorrect, or new password does not match.")
    return render_template("update_password.html", errors=errors)

def has_logged_in():
    return session.get("username", False) != False
