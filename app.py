import os
from config import config
from datetime import timedelta
from flask import Flask, redirect, render_template, request, session
from truenas import TrueNAS

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)
app.config["TRUENAS"] = TrueNAS(config["endpoint"], config["api_key"], config["ignore_invalid_certificate"] != "1")

@app.route("/")
def index():
    if not has_logged_in():
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    errors = []
    if has_logged_in():
        return redirect("/")

    if request.method == "POST" and "username" in request.form and "password" in request.form:
        validate = app.config["TRUENAS"].validate_password(request.form["username"], request.form["password"])
        print("username: " + request.form["username"])

        if validate:
            session.clear()
            user_info = app.config["TRUENAS"].get_user_info(request.form["username"])
            session["user_id"] = user_info[0]["id"]
            session["username"] = user_info[0]["username"]
            return redirect("/")
        
        errors.append("Incorrect username or password.")
    return render_template("login.html", errors=errors)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

def has_logged_in():
    return session.get("username", False) != False
