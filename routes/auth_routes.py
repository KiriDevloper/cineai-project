from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from models.user_model import UserModel

auth_bp = Blueprint(
    "auth",
    __name__
)

# =========================
# REGISTER
# =========================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        # check user exists
        user = UserModel.find_by_username(username)

        if user:
            return "Username already exists"

        new_user = {
            "username": username,
            "password": password
        }

        UserModel.create_user(new_user)

        return redirect("/login")

    return render_template("register.html")

# =========================
# LOGIN
# =========================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = UserModel.find_by_username(username)

        if user and user["password"] == password:

            session["user"] = username

            return redirect("/")

        return "Invalid username or password"

    return render_template("login.html")

# =========================
# LOGOUT
# =========================

@auth_bp.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")